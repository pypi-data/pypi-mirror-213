import apache_beam as beam
from apache_beam.io import ReadFromAvro, WriteToBigQuery, BigQueryDisposition

from ingestor.bq.schemas.providers import get_schema_by_table
from ingestor.bq.options import LoadOptions


def execute_pipeline(options: LoadOptions) -> None:
    schema = get_schema_by_table(options.table)
    file_pattern = f"gs://{options.ingestion_bucket}/**/*.arvo"
    with beam.Pipeline(options=options) as p:
        records = p | "Read files" >> ReadFromAvro(file_pattern=file_pattern)
        records | "WriteDataToBQ" >> WriteToBigQuery(
            table=options.table,
            dataset=options.bq_dataset,
            project=options.bq_project,
            schema=schema,
            method=WriteToBigQuery.Method.STREAMING_INSERTS,
            create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=BigQueryDisposition.WRITE_APPEND,
        )
