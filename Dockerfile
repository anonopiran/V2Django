FROM python:3.10.6-slim AS env
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN apt-get update &&\
    apt-get install --no-install-recommends -y build-essential python3-dev libpq-dev &&\
    pip install micropipenv[toml] --no-input --no-cache-dir && \
    micropipenv install --deploy && \
    pip uninstall micropipenv[toml] --no-input -y --no-cache-dir && \
    apt-get purge -y build-essential python3-dev &&\
    rm -rf /var/lib/apt/lists/*


FROM env AS app
COPY . .
RUN chmod +x ./run.sh
ENTRYPOINT "/bin/bash"
