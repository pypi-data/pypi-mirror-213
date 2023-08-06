import os
from pathlib import Path

import avro.schema


def get_schema_by_table(table: str) -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    schemas = {
        "authors": Path(f"{dir_path}/author.avsc").read_text(),
    }
    if table not in schemas:
        raise ValueError(f"Schema for table {table} is not defined.")
    return avro.schema.parse(schemas[table]).to_json()
