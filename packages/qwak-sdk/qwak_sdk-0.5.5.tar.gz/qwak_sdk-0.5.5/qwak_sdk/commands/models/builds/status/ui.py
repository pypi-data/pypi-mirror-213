import json

import click
from _qwak_proto.qwak.builds.builds_pb2 import BuildStatus
from qwak.tools.logger.logger import get_qwak_logger

from qwak_sdk.commands.models.builds.status._logic import execute_get_build_status
from qwak_sdk.inner.tools.cli_tools import QwakCommand

logger = get_qwak_logger()


@click.command("status", cls=QwakCommand)
@click.argument("build_id")
def get_build_status(build_id, **kwargs):
    if kwargs["format"] == "text":
        logger.info(f"Getting build status for build id [{build_id}]")
    build_status = execute_get_build_status(build_id)
    if kwargs["format"] == "text":
        logger.info(f"Build status: {BuildStatus.Name(build_status)}")
    elif kwargs["format"] == "json":
        print(
            json.dumps(
                {
                    "build_id": build_id,
                    "build_status": BuildStatus.Name(build_status),
                }
            )
        )
    return BuildStatus.Name(build_status)
