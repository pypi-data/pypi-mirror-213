import apache_beam as beam
from apache_beam.io.avroio import WriteToAvro
from beam_nuggets.io import relational_db

from ingestor.gcs.options import IngestionOptions
from ingestor.gcs.schemas.providers import get_schema_by_table


def parse_record(record) -> dict:
    record["registration_date"] = record["registration_date"].timestamp()
    return record


def _get_resulting_path(ingestion_bucket, ingestion_date, table):
    year = ingestion_date[0:4]
    month = ingestion_date[4:6]
    day = ingestion_date[6:8]
    hour = ingestion_date[8:10]
    minute = ingestion_date[10:12]
    return "/".join([
        f"gs://{ingestion_bucket}", table,
        year, month, day, hour, minute,
        f"result-{ingestion_date}-{table}.avro"
    ])


def _get_query(table: str) -> str:
    return f"select * from {table}"


def execute_pipeline(options: IngestionOptions) -> None:
    table = options.table
    schema = get_schema_by_table(table)
    query = _get_query(table)
    result_path = _get_resulting_path(options.ingestion_bucket, options.ingestion_date, table)

    source_config = relational_db.SourceConfiguration(
        drivername="postgresql",
        host=options.host,
        port=options.port,
        username=options.user,
        password=options.password,
        database=options.dbname,
    )

    with beam.Pipeline(options=options) as p:
        records = p | "Reading example records from database" >> relational_db.ReadFromDB(
            source_config=source_config,
            table_name=table,
            query=query
        )
        records | "Parsing records" >> beam.Map(parse_record) \
                | "Write to GCS" >> WriteToAvro(f"{result_path}", schema, file_name_suffix=".arvo")
