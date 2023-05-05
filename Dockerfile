# A simple container for variant-service.
# Runs service on port 80.
# Healthchecks service up every 5m.

FROM python:3.9
RUN apt update && apt install -y rsync python3-dev
RUN pip install uvicorn[standard] websockets
COPY . /app
WORKDIR /app

RUN pip install --pre .
# Run a fork of bioutils
RUN pip install git+https://github.com/theferrit32/bioutils.git@47-large-seq-normalization

EXPOSE 80
HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost/variation || exit 1

# cool-seq-tool initialization involves writing some files and this doesn't
# work sometimes if multiple worker processes are in that step at the same time
# limit to 1 worker process for now
CMD python -c "import cool_seq_tool" && uvicorn variation.main:app --workers 4 --port 80 --host 0.0.0.0
