import logging

from .daemon_info import DockerDaemonInfo
from .run_builder import DockerRunBuilder
from ..process_utils import run_process


logger = logging.getLogger(__name__)


class RootlessDockerContainer(object):
    """

    """
    def __init__(self, container_name: str, daemon_info: DockerDaemonInfo):
        self.container_name = container_name
        self._daemon_info = daemon_info

    def does_rootless_container_exist(self) -> bool:
        for c in self._daemon_info.containers:
            if self.container_name == c['Names']:
                return True
        return False

    def is_rootless_container_running(self) -> bool:
        logger.debug(f'Listing all containers')
        for c in self._daemon_info.containers:
            logger.debug(c)
            if self.container_name == c['Names'] and 'running' == c['State']:
                return True
        return False

    def is_rootless_container_not_running(self) -> bool:
        for c in self._daemon_info.containers:
            logger.info(c)
            if self.container_name == c['Names'] and 'running' != c['State']:
                return True
        return False

    def start_rootless_container(self, workspace_path: str, network_name: str) -> None:
        logger.debug(f'Testing if rootless is running')
        if self.is_rootless_container_running():
            logger.info(f'Rootless container {self.container_name}')
            return

        if self.is_rootless_container_not_running():
            logger.info(f'Killing dead rootless container {self.container_name}')
            for log_line in run_process(f'docker rm -f {self.container_name}'):
                logger.info(log_line)

        run_rootless_docker_cmd = DockerRunBuilder('docker:23.0.1-dind-rootless')
        run_rootless_docker_cmd.options() \
            .with_name(self.container_name) \
            .with_hostname(self.container_name) \
            .with_privileged() \
            .with_daemon() \
            .with_user() \
            .with_env('DOCKER_TLS_CERTDIR', '') \
            .with_port_mapping(2375, 2375) \
            .with_port_mapping(80, 80) \
            .with_bind_mount(workspace_path, workspace_path) \
            .with_bind_mount('/tmp', '/tmp') \
            .with_bind_mount('/dev', '/dev') \
            .with_named_volume('rootless-storage', '/var/lib/docker') \
            .with_named_volume('rootless-user-storage', '/home/rootless/.local/share/docker') \
            .with_mount_home() \
            .with_network(network_name)

        for log_line in run_process(run_rootless_docker_cmd.build()):
            logger.info(log_line)
