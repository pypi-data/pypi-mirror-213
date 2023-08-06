import click

from ingestor.gcs.ingestion import execute_pipeline
from ingestor.gcs.options import IngestionOptions


@click.command("ingest")
@click.option(
    "--host",
    default="localhost",
    help="The host of the database to connect to."
)
@click.option(
    "--port",
    default="5432",
    help="The port of the database to connect to."
)
@click.option(
    "--user",
    default="postgres",
    help="The user of the database to connect to."
)
@click.password_option(
    "--password",
    default="postgres",
    confirmation_prompt=False,
    help="The password of the database to connect to."
)
@click.option(
    "--dbname",
    default="postgres",
    help="The name of the database to connect to."
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
@click.option(
    "--runner",
    required=False,
    default="DirectRunner",
    help="The runner to use for the pipeline."
)
@click.option(
    "--project",
    required=False,
    help="The project to use for the pipeline."
)
@click.option(
    "--region",
    required=False,
    help="The region to use for the pipeline."
)
@click.option(
    "--temp_location",
    required=False,
    help="The temp location to use for the pipeline."
)
@click.option(
    "--staging_location",
    required=False,
    help="The staging location to use for the pipeline."
)
@click.option(
    "--experiments",
    required=False,
    default="use_runner_v2",
    help="The experiments to use for the pipeline."
)
@click.option(
    "--sdk_location",
    required=False,
    help="The sdk location to use for the pipeline."
)
@click.option(
    "--sdk_container_image",
    required=False,
    help="The sdk container image to use for the pipeline."
)
def ingest(
    host: str,
    port: str,
    user: str,
    password: str,
    dbname: str,
    table: str,
    ingestion_bucket: str,
    save_main_session: bool,
    runner: str,
    project: str,
    region: str,
    temp_location: str,
    staging_location: str,
    experiments: str,
    sdk_location: str,
    sdk_container_image: str,
):
    click.echo("Starting ingestion pipeline...")
    options = IngestionOptions.from_dictionary({
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "dbname": dbname,
        "table": table,
        "ingestion_bucket": ingestion_bucket,
        "save_main_session": save_main_session,
        "runner": runner,
        "project": project,
        "region": region,
        "temp_location": temp_location,
        "staging_location": staging_location,
        "experiments": experiments,
        "sdk_location": sdk_location,
        "sdk_container_image": sdk_container_image,
    })
    execute_pipeline(options)
    click.echo("Ingestion pipeline finished.")
