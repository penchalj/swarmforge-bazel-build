# Runtime image: only the fusion_node binary on a pinned Ubuntu base.
# No compiler, no build tools. The binary is built and tested by Bazel.
FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

LABEL org.opencontainers.image.source="https://github.com/penchalj/swarmforge" \
      org.opencontainers.image.description="SwarmForge fusion-node" \
      org.opencontainers.image.licenses="Apache-2.0"

COPY --chmod=0755 fusion_node /usr/local/bin/fusion_node

# Non-root: the "ubuntu" user (UID 1000) already exists in this base image.
USER ubuntu
ENTRYPOINT ["/usr/local/bin/fusion_node"]
