from typing import Tuple

from qwak.clients.batch_job_management import BatchJobManagerClient
from qwak.clients.batch_job_management.executions_config import ExecutionConfig
from qwak.clients.batch_job_management.results import StartExecutionResult
from qwak.clients.instance_template.client import InstanceTemplateManagementClient

from qwak_sdk.commands.models._logic.instance_template import verify_template_id


def execute_start_execution(config: ExecutionConfig) -> Tuple[str, bool, str]:
    if config.resources.instance_size:
        verify_template_id(
            config.resources.instance_size, InstanceTemplateManagementClient()
        )
    batch_job_start_response: StartExecutionResult = (
        BatchJobManagerClient().start_execution(config)
    )
    return (
        batch_job_start_response.execution_id,
        batch_job_start_response.success,
        batch_job_start_response.failure_message,
    )
