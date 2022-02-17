FROM python:3.9-slim as build-image
RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential gcc \
&& apt-get clean

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

FROM python:3.9-slim as production-image
COPY --from=build-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./app /app
WORKDIR /app

ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port $PORT