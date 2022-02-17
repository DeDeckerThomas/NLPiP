FROM nvcr.io/nvidia/tritonserver:21.12-py3

COPY ./core /core

RUN pip install -r /core/requirements.txt && mkdir /home/triton-server && chown triton-server /home/triton-server

USER triton-server