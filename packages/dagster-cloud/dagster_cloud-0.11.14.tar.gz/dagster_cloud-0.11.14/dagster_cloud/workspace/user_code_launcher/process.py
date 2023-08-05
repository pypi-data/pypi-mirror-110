import subprocess
import sys
import threading
from collections import namedtuple
from typing import List

from dagster import check
from dagster.core.events import DagsterEvent
from dagster.core.executor.step_delegating import StepHandler
from dagster.core.executor.step_delegating.step_handler.base import StepHandlerContext
from dagster.core.host_representation.grpc_server_registry import GrpcServerEndpoint
from dagster.core.launcher import DefaultRunLauncher
from dagster.core.types.loadable_target_origin import LoadableTargetOrigin
from dagster.daemon.daemon import get_default_daemon_logger
from dagster.grpc.client import DagsterGrpcClient, client_heartbeat_thread
from dagster.grpc.server import GrpcServerProcess
from dagster.serdes import ConfigurableClass, create_snapshot_id, serialize_dagster_namedtuple

from .user_code_launcher import ReconcileUserCodeLauncher


class ProcessUserCodeEntry(
    namedtuple(
        "_ProcessUserCodeEntry",
        "grpc_server_process grpc_client heartbeat_shutdown_event heartbeat_thread",
    )
):
    def __new__(cls, grpc_server_process, grpc_client, heartbeat_shutdown_event, heartbeat_thread):
        return super(ProcessUserCodeEntry, cls).__new__(
            cls,
            check.inst_param(grpc_server_process, "grpc_server_process", GrpcServerProcess),
            check.inst_param(grpc_client, "grpc_client", DagsterGrpcClient),
            check.inst_param(heartbeat_shutdown_event, "heartbeat_shutdown_event", threading.Event),
            check.inst_param(heartbeat_thread, "heartbeat_thread", threading.Thread),
        )


class ProcessUserCodeLauncher(ReconcileUserCodeLauncher, ConfigurableClass):
    def __init__(self, inst_data=None, graphql_client=None, wait_for_processes=False):
        self._inst_data = inst_data
        self._logger = get_default_daemon_logger("ProcessDagsterUserCodeLauncher")

        # Dict[int, ProcessUserCodeEntry], map from pid to all servers being spun up (including
        # old servers in the process of being shut down)
        self._process_entries = {}

        # Dict[str, int], map from hash of location_name + metadata (see _get_process_key)
        # to the pid for that location-metadata combination
        self._active_pids = {}

        self._heartbeat_ttl = 60
        self._wait_for_processes = wait_for_processes

        super(ProcessUserCodeLauncher, self).__init__(graphql_client=graphql_client)

        self._launcher = DefaultRunLauncher()

    def register_instance(self, instance):
        super().register_instance(instance)
        self._launcher.register_instance(instance)

    @property
    def inst_data(self):
        return self._inst_data

    @classmethod
    def config_type(cls):
        return {}

    @staticmethod
    def from_config_value(inst_data, config_value):
        return ProcessUserCodeLauncher(inst_data=inst_data)

    def _add_server(self, location_name, metadata):
        process_key = self._get_process_key(location_name, metadata)
        existing_pid = self._get_existing_pid(location_name, metadata)
        if existing_pid:
            self._remove_pid(existing_pid)
            del self._active_pids[process_key]

        return self._start_new_server(location_name, metadata)

    def _start_new_server(self, location_name, metadata):
        process_key = self._get_process_key(location_name, metadata)
        loadable_target_origin = self._get_loadable_target_origin(metadata)
        server_process = GrpcServerProcess(
            loadable_target_origin=loadable_target_origin,
            heartbeat=True,
            heartbeat_timeout=self._heartbeat_ttl,
        )
        server_id = self._wait_for_server(
            host="localhost", port=server_process.port, socket=server_process.socket
        )

        client = DagsterGrpcClient(
            port=server_process.port,
            socket=server_process.socket,
            host="localhost",
            use_ssl=False,
        )

        heartbeat_shutdown_event = threading.Event()
        heartbeat_thread = threading.Thread(
            target=client_heartbeat_thread,
            args=(client, heartbeat_shutdown_event),
        )
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

        pid = server_process.pid

        self._process_entries[server_process.pid] = ProcessUserCodeEntry(
            server_process,
            client,
            heartbeat_shutdown_event,
            heartbeat_thread,
        )
        self._active_pids[process_key] = pid

        endpoint = GrpcServerEndpoint(
            server_id=server_id,
            host="localhost",
            port=server_process.port,
            socket=server_process.socket,
        )

        return endpoint

    def _get_process_key(self, location_name, metadata):
        return f"{location_name}_{create_snapshot_id(metadata)[0:6]}"

    def _get_loadable_target_origin(self, metadata):
        return LoadableTargetOrigin(
            executable_path=sys.executable,
            python_file=metadata.python_file,
            package_name=metadata.package_name,
        )

    def _get_existing_pid(self, location_name, metadata):
        process_key = self._get_process_key(location_name, metadata)
        return self._active_pids.get(process_key)

    def _gen_update_server(self, location_name, old_metadata, new_metadata):
        old_process_key = self._get_process_key(location_name, old_metadata)
        new_process_key = self._get_process_key(location_name, new_metadata)
        existing_pid = self._get_existing_pid(location_name, old_metadata)

        updated_server = self._start_new_server(location_name, new_metadata)
        yield updated_server

        if existing_pid:
            self._logger.info(
                "Stopping old process for location {location_name}".format(
                    location_name=location_name,
                )
            )
            self._remove_pid(existing_pid)
            if old_process_key != new_process_key:
                del self._active_pids[old_process_key]

    def _remove_server(self, location_name, metadata):
        process_key = self._get_process_key(location_name, metadata)
        existing_pid = self._get_existing_pid(location_name, metadata)
        if existing_pid:
            self._logger.info(
                "Stopping process for location {location_name}".format(
                    location_name=location_name,
                )
            )
            self._remove_pid(existing_pid)
            del self._active_pids[process_key]

    def _remove_pid(self, pid):
        process_entry = self._process_entries[pid]
        process_entry.heartbeat_shutdown_event.set()
        process_entry.heartbeat_thread.join()
        # Rely on heartbeat failure to eventually kill the process
        del self._process_entries[pid]

    def step_handler(self):
        return ProcessStepHandler()

    def run_launcher(self):
        return self._launcher

    def __exit__(self, exception_type, exception_value, traceback):
        self._launcher.dispose()
        while len(self._process_entries):
            pid = next(iter(self._process_entries))
            process_entry = self._process_entries[pid]

            self._remove_pid(pid)
            if self._wait_for_processes:
                process_entry.grpc_client.shutdown_server()
                process_entry.grpc_server_process.wait()


class ProcessStepHandler(StepHandler):
    @property
    def name(self) -> str:
        return "ProcessStepHandler"

    def launch_step(self, step_handler_context: StepHandlerContext) -> List[DagsterEvent]:
        input_json = serialize_dagster_namedtuple(step_handler_context.execute_step_args)
        args = ["dagster", "api", "execute_step", input_json]
        subprocess.Popen(args)
        return []

    def check_step_health(self, step_handler_context: StepHandlerContext) -> List[DagsterEvent]:
        # TODO not implemented
        return []

    def terminate_step(self, step_handler_context: StepHandlerContext) -> List[DagsterEvent]:
        # TODO not implemented
        return []
