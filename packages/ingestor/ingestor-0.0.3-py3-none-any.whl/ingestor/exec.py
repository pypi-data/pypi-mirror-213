import argparse
import sys

from apache_beam.options.pipeline_options import SetupOptions

from gcs.ingestion import execute_pipeline
from gcs.options import IngestionOptions


def main(argv):
    parser = argparse.ArgumentParser()
    pipeline_options, pipeline_args = parser.parse_known_args(argv)
    options = IngestionOptions(pipeline_args)
    options.view_as(SetupOptions).save_main_session = True
    execute_pipeline(options)


if __name__ == "__main__":
    main(sys.argv)
