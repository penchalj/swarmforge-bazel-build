# ADR 0007: Licence policy gate on shipped images

## Context
Every image now has SPDX and CycloneDX SBOMs (ADR 0005), but nothing checked
the licences in them. A customer or auditor needs to know that a release does
not ship code under licences the product cannot accept, and that this is
enforced by the pipeline rather than by a manual review.

Both runtime images use distribution base images (Ubuntu 24.04 and Debian
python:3.12-slim). These contain GPL-licensed tools such as bash, coreutils
and tar. A flat rule "GPL fails the build" would fail on every run and would
be switched off within a week.

## Decision
1. **Two scopes.** Each SBOM component is classified by its Syft package type:
   - *Base layer* (deb, apk, rpm, classifier-detected binaries): unmodified
     distribution packages, used as separate programs; source is available from
     the distribution. Only `deny_everywhere` applies (AGPL, SSPL, BUSL,
     Commons Clause). GPL packages are counted in the report, not blocked.
   - *Application* (everything we add: pip packages today, Conan or other
     package managers later): GPL, AGPL, SSPL, BUSL and non-commercial
     licences fail; a missing licence fails; LGPL, MPL, EPL and CDDL are
     reported for review.
2. **Correct SPDX expressions.** `A OR B` fails only if every option is denied
   (we may choose), `A AND B` fails if any part is denied, `WITH` exceptions
   keep the base licence.
3. **Policy as code.** [licence-policy.json](../../licence-policy.json) is
   reviewed like any other change. Exceptions need a purl prefix, a reason and
   an approver.
4. **Gate before publish.** The check runs in the Images job before anything
   is pushed, so it is part of the required checks on `main` and a violating
   image is never published or released.
5. **Own small tool instead of grant or ScanCode.** grant's policy cannot
   separate base-layer packages from application packages, and ScanCode scans
   source trees, which is slow and duplicates what Syft already found. A
   small Python checker with unit tests reads the CycloneDX SBOM we already
   produce. It runs with the system Python, with no extra download to pin.

## Consequences
+ A copyleft or unlicensed dependency added to application code fails the PR
+ The report (job summary) lists violations, review items and the number of
  copyleft base-layer packages
- Base-layer GPL packages are accepted by policy, not removed. Moving to
  distroless or scratch runtime images would remove most of them.
- Libraries statically linked into the C++ binary by Bazel (protobuf, abseil,
  libc++) are invisible to Syft, so they are not checked. A Bazel-level SBOM
  (see README, "What remains") would close this gap.
- Package metadata can be wrong or missing; a false "no licence found" is
  fixed with a reviewed exception, not by weakening the policy.

## Alternatives considered
- **grant (Anchore):** good fit for Syft SBOMs, but no scope by package type.
  Revisit if it gains that.
- **ScanCode Toolkit:** most thorough (scans file contents), useful for our own
  source tree; too slow and too broad for an image gate.
- **FOSSA / Black Duck:** commercial; same idea with a managed licence
  database and legal workflow.
