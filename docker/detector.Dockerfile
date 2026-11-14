# Runtime image for the Python detector. The protobuf Python package must match
# the Bazel-generated code: protobuf 29.x <-> Python package 5.29.x (>= 5.29.3).
FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b

LABEL org.opencontainers.image.source="https://github.com/penchalj/swarmforge" \
      org.opencontainers.image.description="SwarmForge synthetic detector" \
      org.opencontainers.image.licenses="Apache-2.0"

RUN pip install --no-cache-dir protobuf==5.29.6 \
    && pip uninstall -y pip \
    && mkdir -p /data && chown nobody:nogroup /data

WORKDIR /app
COPY app/ /app/

USER nobody
ENTRYPOINT ["python", "-m", "detector.sim_detector"]
