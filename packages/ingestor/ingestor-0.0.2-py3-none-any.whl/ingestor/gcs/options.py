import datetime

from apache_beam.options.pipeline_options import _BeamArgumentParser

from common_options import CommonOptions


class IngestionOptions(CommonOptions):

    @classmethod
    def _add_argparse_args(cls, parser: _BeamArgumentParser) -> None:
        parser.add_argument("--host", required=True)
        parser.add_argument("--port", required=False, default="5432", type=int)
        parser.add_argument("--user", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--dbname", required=True)
        parser.add_argument(
            "--ingestion_date",
            required=False,
            default=datetime.datetime.now().strftime("%Y%m%d%H%M")
        )
        parser.add_argument("--runner", required=False)
        parser.add_argument("--project", required=False)
        parser.add_argument("--region", required=False)
        parser.add_argument("--temp_location", required=False)
        parser.add_argument("--staging_location", required=False)
        # parser.add_argument("--save_main_session", required=False, default=True)
