from apache_beam.options.pipeline_options import _BeamArgumentParser

from common_options import CommonOptions


class LoadOptions(CommonOptions):
    @classmethod
    def _add_argparse_args(cls, parser: _BeamArgumentParser) -> None:
        parser.add_argument("--bq_project", required=True)
        parser.add_argument("--bq_dataset", required=True)
        # parser.add_argument("--ingestion_date", required=True)
