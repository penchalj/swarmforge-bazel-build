# Pinned build environment: same image for laptops and CI, amd64 and arm64.
# The digest is a multi-arch index; Docker picks the right variant per machine.
FROM ubuntu:24.04@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac

# libc6-dev + libgcc-13-dev = the target system's C library headers and startup
# files (the "sysroot"). The compiler itself comes from Bazel's pinned LLVM.
# clang-format-18 and shellcheck are linters only; no compiler is installed.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git python3 libxml2 \
        libc6-dev libgcc-13-dev \
        clang-format-18 shellcheck \
    && rm -rf /var/lib/apt/lists/*

# Pinned tools, downloaded for the image's own CPU architecture.
ARG TARGETARCH
RUN case "${TARGETARCH}" in \
      amd64) arch=amd64; ruff_arch=x86_64 ;; \
      arm64) arch=arm64; ruff_arch=aarch64 ;; \
      *) echo "unsupported architecture: ${TARGETARCH}" >&2; exit 1 ;; \
    esac \
    && curl -fsSL -o /usr/local/bin/bazel \
         "https://github.com/bazelbuild/bazelisk/releases/download/v1.25.0/bazelisk-linux-${arch}" \
    && curl -fsSL -o /usr/local/bin/buildifier \
         "https://github.com/bazelbuild/buildtools/releases/download/v7.3.1/buildifier-linux-${arch}" \
    && curl -fsSL "https://github.com/astral-sh/ruff/releases/download/0.6.9/ruff-${ruff_arch}-unknown-linux-gnu.tar.gz" \
         | tar -xz -C /usr/local/bin --strip-components=1 "ruff-${ruff_arch}-unknown-linux-gnu/ruff" \
    && chmod +x /usr/local/bin/bazel /usr/local/bin/buildifier

# Writable home and cache for any user ID (CI runners use UID 1001, laptops 1000)
RUN mkdir -p /home/ubuntu/.cache \
    && chown -R ubuntu:ubuntu /home/ubuntu/.cache \
    && chmod 1777 /home/ubuntu /home/ubuntu/.cache
USER ubuntu
WORKDIR /workspace
