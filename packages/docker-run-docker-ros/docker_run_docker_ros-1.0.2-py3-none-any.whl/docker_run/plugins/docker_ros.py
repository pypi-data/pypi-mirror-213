import argparse
import os
from typing import Any, Dict, List

from docker_run.utils import runCommand
from docker_run.plugins.plugin import Plugin


__version__ = "1.0.2"


class DockerRosPlugin(Plugin):

    TARGET_MOUNT = "/docker-ros/ws/src/target"

    @classmethod
    def addArguments(cls, parser: argparse.ArgumentParser):

        prefix = "[docker-ros]"

        parser.add_argument("--no-user", action="store_true", help=f"{prefix} disable passing local UID/GID into container")
        parser.add_argument("--mws", action="store_true", help=f"{prefix} mount current directory into ROS workspace at `{cls.TARGET_MOUNT}`")

    @classmethod
    def getRunFlags(cls, args: Dict[str, Any], unknown_args: List[str]) -> List[str]:
        flags = []
        if not args["no_user"]:
            flags += cls.userFlags()
        if args["mws"]:
            flags += cls.currentDirMountWorkspaceFlags()
        return flags

    @classmethod
    def getExecFlags(cls, args: Dict[str, Any], unknown_args: List[str]) -> List[str]:
        flags = []
        is_docker_ros = (runCommand(f"docker exec {args['name']} printenv DOCKER_ROS")[0][:-1] == "1")
        is_non_root = (len(runCommand(f"docker exec {args['name']} printenv DOCKER_UID")[0][:-1]) > 0)
        if not args["no_user"] and is_docker_ros and is_non_root:
            flags += cls.userExecFlags()
        return flags

    @classmethod
    def userFlags(cls) -> List[str]:
        return [f"--env DOCKER_UID={os.getuid()}", f"--env DOCKER_GID={os.getgid()}"]

    @classmethod
    def userExecFlags(cls) -> List[str]:
        return [f"--user {os.getuid()}"]

    @classmethod
    def currentDirMountWorkspaceFlags(cls) -> List[str]:
        return [f"--volume {os.getcwd()}:{cls.TARGET_MOUNT}"]
