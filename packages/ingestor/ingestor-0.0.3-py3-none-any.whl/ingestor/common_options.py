from apache_beam.options.pipeline_options import PipelineOptions, _BeamArgumentParser


class CommonOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser: _BeamArgumentParser) -> None:
        parser.add_argument("--table", required=True)
        parser.add_argument("--ingestion_bucket", required=True)
