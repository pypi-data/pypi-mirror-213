FROM apache/beam_python3.9_sdk:2.47.0

LABEL language="Python3"
LABEL engine="Dataflow"

RUN pip3 install --upgrade pip
RUN pip3 install "poetry>=1.0.5,<2.0.0"
RUN pip3 install ingestor==0.0.2

CMD ["/bin/sh"]
