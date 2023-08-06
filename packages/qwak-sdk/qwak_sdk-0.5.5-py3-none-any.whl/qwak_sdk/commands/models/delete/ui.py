import click

from qwak_sdk.commands.models.delete._logic import execute_model_delete
from qwak_sdk.commands.ui_tools import output_as_json
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command("delete", cls=QwakCommand)
@click.option("--project-id", metavar="NAME", required=True, help="Project id")
@click.option("--model-id", metavar="NAME", required=True, help="Model name")
def model_delete(project_id, model_id, **kwargs):
    response = execute_model_delete(project_id, model_id)
    if kwargs["format"] == "json":
        output_as_json(response)
    else:
        print(f"Model deleted\nmodel id : {model_id}")
