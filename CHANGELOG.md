# Changelog

## [0.1.2](https://github.com/penchalj/swarmforge-bazel-build/compare/v0.1.1...v0.1.2) (2026-11-09)


### Build System

* bump python from `a6e34c5` to `aa943ce` in /docker ([c35955c](https://github.com/penchalj/swarmforge-bazel-build/commit/c35955cc9f21814362877f898adac94136f7cf43))
* bump ubuntu from `534baea` to `68ee220` in /docker ([c874f07](https://github.com/penchalj/swarmforge-bazel-build/commit/c874f074401ddd65ef96d29c9c80af24cd27b7a6))


### Continuous Integration

* add licence checker, policy and ADR 0007 ([c2b2f6e](https://github.com/penchalj/swarmforge-bazel-build/commit/c2b2f6e8137712dfee79b78b11b8df6baee48f26))


### Documentation

* add introduction, objective, progress, approach and tools to README ([#32](https://github.com/penchalj/swarmforge-bazel-build/issues/32)) ([fa1579d](https://github.com/penchalj/swarmforge-bazel-build/commit/fa1579d7b7102fc8e89ff0aeaacefe326811bc39))
* add README with results, architecture and role mapping ([#31](https://github.com/penchalj/swarmforge-bazel-build/issues/31)) ([fc1b46d](https://github.com/penchalj/swarmforge-bazel-build/commit/fc1b46d1ab594895efb80ce7b18840f5d2fac4fd))
* add release and rollback drill, failure lab entries 9-11 ([#29](https://github.com/penchalj/swarmforge-bazel-build/issues/29)) ([66282e1](https://github.com/penchalj/swarmforge-bazel-build/commit/66282e1805bc5590cd4878427b4c524be698f601))
* list requirements for the try-it guide ([#33](https://github.com/penchalj/swarmforge-bazel-build/issues/33)) ([f5bc0e9](https://github.com/penchalj/swarmforge-bazel-build/commit/f5bc0e9abb7b611ae956f678ad84f27148fd3e04))

## [0.1.1](https://github.com/penchalj/swarmforge/compare/v0.1.0...v0.1.1) (2026-10-11)


### Bug Fixes

* **forge:** clearer disk space hint ([#27](https://github.com/penchalj/swarmforge/issues/27)) ([d0e65d0](https://github.com/penchalj/swarmforge/commit/d0e65d071f265eda1c0deee72c6068d1dda41a1c))

## 0.1.0 (2026-10-11)


### Features

* add sanitizer lane (ASan, UBSan with canaries), native arm64 build and QEMU edge smoke test ([903437b](https://github.com/penchalj/swarmforge/commit/903437ba66e4f0cd711a5e232d8f29fc0684820f))
* add shared detection proto, C++ fusion-node and Python detector ([91027ec](https://github.com/penchalj/swarmforge/commit/91027ecef7230ce8fab8586778994e863dff0a21))
* automated releases with release-please and promotion by digest with approval ([93af0f5](https://github.com/penchalj/swarmforge/commit/93af0f5bbc5624e06b2592f1943f4edcbad644d7))
* **detector:** make sensor name configurable ([#1](https://github.com/penchalj/swarmforge/issues/1)) ([b541de1](https://github.com/penchalj/swarmforge/commit/b541de1d86d893c499fca446a7c7d5e013e34b75))
* **forge:** add forge doctor to check developer machines ([#22](https://github.com/penchalj/swarmforge/issues/22)) ([a7992a0](https://github.com/penchalj/swarmforge/commit/a7992a0f4b96ea40a846f0b6c565573707737a88))
* **libtrack:** Kalman tracker with hermetic LLVM build in pinned container ([6820403](https://github.com/penchalj/swarmforge/commit/6820403e910b8e508677b0edfb884b09c647cd23))
* release images with Compose test, SBOM, vulnerability gate and cosign keyless signing ([6cd2813](https://github.com/penchalj/swarmforge/commit/6cd2813239d37a614276f317f0a8c013578c6879))


### Build System

* add pinned lint tools and CI-ready dev.sh ([43ad4da](https://github.com/penchalj/swarmforge/commit/43ad4dab269ce192af820a5a5d9c7109e46a83af))
* pin base image digest, add rules_python and protobuf ([b2baa0b](https://github.com/penchalj/swarmforge/commit/b2baa0b866e9d42562bda02f69347c15dbb8a5cd))
* start release-please at version 0.1.0 ([#25](https://github.com/penchalj/swarmforge/issues/25)) ([c372924](https://github.com/penchalj/swarmforge/commit/c372924e53800b91c186407c8cade6c28408fdb4))


### Continuous Integration

* add Dependabot for GitHub Actions updates ([#3](https://github.com/penchalj/swarmforge/issues/3)) ([5a8b536](https://github.com/penchalj/swarmforge/commit/5a8b5362e8816c4c1eba9baed9ed71d2504e7aae))
* add GitHub Actions pipeline with lint, affected tests and Bazel cache ([ff3ec4d](https://github.com/penchalj/swarmforge/commit/ff3ec4dc0b3bdbb1ded4513d2abb187a00a015e0))
* bump actions/cache from 4 to 6 ([#4](https://github.com/penchalj/swarmforge/issues/4)) ([9f47aa7](https://github.com/penchalj/swarmforge/commit/9f47aa735d49460d7dc79095cce119b8227f9ef5))
* bump actions/checkout from 4 to 7 ([#7](https://github.com/penchalj/swarmforge/issues/7)) ([8082f6c](https://github.com/penchalj/swarmforge/commit/8082f6cdbbc097bfb42860a256640b25885e4f21))
* bump actions/download-artifact from 4 to 8 ([#17](https://github.com/penchalj/swarmforge/issues/17)) ([954a93c](https://github.com/penchalj/swarmforge/commit/954a93c1aaf5e2f088b73aa19531f0c75a3a6579))
* bump actions/upload-artifact from 4 to 7 ([#16](https://github.com/penchalj/swarmforge/issues/16)) ([57920cf](https://github.com/penchalj/swarmforge/commit/57920cfeda83036b6500a306d2a32e0ab21f8e9b))
* bump anchore/scan-action from 5 to 7 ([#14](https://github.com/penchalj/swarmforge/issues/14)) ([60e38b8](https://github.com/penchalj/swarmforge/commit/60e38b89a27c70fffc901d0dd17479486f94e3db))
* bump docker/build-push-action from 6 to 7 ([#6](https://github.com/penchalj/swarmforge/issues/6)) ([520078f](https://github.com/penchalj/swarmforge/commit/520078fe1739f1f441e7bfe07e2e00392f3bffc1))
* bump docker/login-action from 3 to 4 ([#15](https://github.com/penchalj/swarmforge/issues/15)) ([7a76a7a](https://github.com/penchalj/swarmforge/commit/7a76a7ac0bf61fa442ccdef50668e0377914827f))
* bump docker/setup-buildx-action from 3 to 4 ([#5](https://github.com/penchalj/swarmforge/issues/5)) ([4622e50](https://github.com/penchalj/swarmforge/commit/4622e508bb923806f4c7bfed5736eb071c97957c))
* bump docker/setup-qemu-action from 3 to 4 ([#13](https://github.com/penchalj/swarmforge/issues/13)) ([9d43952](https://github.com/penchalj/swarmforge/commit/9d439525664557ab547444aea345e3e2cc324124))
* cancel superseded runs only on pull requests ([#8](https://github.com/penchalj/swarmforge/issues/8)) ([f8cebb7](https://github.com/penchalj/swarmforge/commit/f8cebb7de799e737c55b46c914af4786c8de98a3))
* give every main commit its own concurrency group so no main run is dropped ([#19](https://github.com/penchalj/swarmforge/issues/19)) ([f3c0d1e](https://github.com/penchalj/swarmforge/commit/f3c0d1ef6a58beeb8283a30f3466e9f72f4b87c1))
* keep Dependabot to digest updates for OS and Python base images ([#18](https://github.com/penchalj/swarmforge/issues/18)) ([3f6f3a0](https://github.com/penchalj/swarmforge/commit/3f6f3a01b8ef69509651da77af288912ec89616f))
* keep Dependabot to digest updates for OS and Python base images ([#20](https://github.com/penchalj/swarmforge/issues/20)) ([80d56d4](https://github.com/penchalj/swarmforge/commit/80d56d4a0dcffa436ec94d6aba0bdcda4384a712))
* require Conventional Commit PR titles for correct changelogs ([#26](https://github.com/penchalj/swarmforge/issues/26)) ([71c195e](https://github.com/penchalj/swarmforge/commit/71c195e2bf573ccfc64b157b1162b0ea632c6d12))


### Tests

* **libtrack:** mark kalman_cv_test as small ([72a0b34](https://github.com/penchalj/swarmforge/commit/72a0b3482e67890d621f0178a7a36936120113e1))


### Documentation

* add ADR 0003 on CI design ([#2](https://github.com/penchalj/swarmforge/issues/2)) ([b5aa474](https://github.com/penchalj/swarmforge/commit/b5aa4744b4b34399360f8abbcfb26acf6943885e))
* add CI timings table ([a9e4d95](https://github.com/penchalj/swarmforge/commit/a9e4d95287bd0a6d23cedcee61e85440708104c6))
* add devcontainer and ADR 0002 on file-based proto exchange ([a268eef](https://github.com/penchalj/swarmforge/commit/a268eef821c99bc1815dc14315a530a22997ba77))
* add failure lab entries 6-8 and image pipeline timings ([#21](https://github.com/penchalj/swarmforge/issues/21)) ([197f44f](https://github.com/penchalj/swarmforge/commit/197f44f9baba0ab4529f98113f2d2a21e7d09154))
* **failure-lab:** add entry 5, protobuf 31 vs libc++ 17 ([8f701d6](https://github.com/penchalj/swarmforge/commit/8f701d628ba4fe2546c6d629dc6a9b2ce671d3e9))
* record full lane CI timings ([#10](https://github.com/penchalj/swarmforge/issues/10)) ([c55d094](https://github.com/penchalj/swarmforge/commit/c55d094c6853ff01c0697c11fc646ab785d40ef5))
