import click

from ingestor.bq.load import execute_pipeline
from ingestor.bq.options import LoadOptions


@click.command("load")
@click.option(
    "--bq_project",
    required=True,
    help="The name of the BigQuery project to connect to."
)
@click.option(
    "--bq_dataset",
    required=True,
    help="The name of the BigQuery dataset to connect to."
)
@click.option(
    "--table",
    required=True,
    help="The name of the table to connect to."
)
@click.option(
    "--ingestion_bucket",
    required=True,
    help="The name of the ingestion bucket containing the data to load."
)
@click.option(
    "--save_main_session",
    required=False,
    default=True,
    help="Whether to save the main session state or not."
)
def load(
    bq_project: str,
    bq_dataset: str,
    table: str,
    ingestion_bucket: str,
    save_main_session: bool,
):
    click.echo("Starting ingestion pipeline...")
    options = LoadOptions.from_dictionary({
        "bq_project": bq_project,
        "bq_dataset": bq_dataset,
        "table": table,
        "ingestion_bucket": ingestion_bucket,
        "save_main_session": save_main_session
    })
    execute_pipeline(options)
    click.echo("Ingestion pipeline finished.")
