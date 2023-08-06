import click

from qwak_sdk.commands.models.runtime.feedback._logic import FeedbackClient
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command("feedback", cls=QwakCommand)
@click.option("--model-id", help="Model ID", required=True)
@click.option(
    "--analytics-entity-column", required=True, help="Analytics entity column name"
)
@click.option(
    "--feedback-entity-column", required=True, help="Feedback entity column name"
)
@click.option(
    "--model-type",
    required=True,
    type=click.Choice(
        ["binary_classification", "multiclass_classification", "regression"],
        case_sensitive=True,
    ),
    help="""Model type. Options: binary_classification / multiclass_classification / regression""",
)
@click.option(
    "--feedback-config",
    help="Feedback configuration. analytics_output_column=actual_tag",
    metavar="ANALYTICS_OUTPUT_COLUMN=ACTUAL_TAG",
    multiple=True,
)
def runtime_feedback(
    model_id,
    analytics_entity_column,
    feedback_entity_column,
    model_type,
    feedback_config,
    **kwargs,
):
    feedback_client = FeedbackClient(model_id=model_id)
    response = feedback_client.config(
        analytics_entity_column=analytics_entity_column,
        feedback_entity_column=feedback_entity_column,
        model_type=model_type,
        feedback_config=feedback_config,
    )
    print(response)
