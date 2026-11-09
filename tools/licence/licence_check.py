"""Licence policy check for CycloneDX SBOMs produced by Syft.

Usage:
    python3 tools/licence/licence_check.py --policy licence-policy.json \
        sbom-fusion-node-amd64.cdx.json sbom-detector-amd64.cdx.json

Every component is put in one of two scopes:
  * base layer: packages that come with the OS base image (deb, apk, rpm and
    binaries Syft finds by classifier, e.g. the Python interpreter). These are
    unmodified distribution packages; only the "deny_everywhere" list applies.
  * application: everything we add ourselves (pip packages today; Conan, npm
    or Cargo packages later). The full deny list applies, unknown licences fail
    and weak-copyleft licences are reported for review.

Exit code 0 = policy passed, 1 = violations, 2 = usage or input error.
A Markdown report is appended to $GITHUB_STEP_SUMMARY when it is set.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

UNKNOWN = "UNKNOWN"
_TOKEN = re.compile(r"\(|\)|\bAND\b|\bOR\b|\bWITH\b|[^\s()]+")


@dataclass
class Finding:
    sbom: str
    name: str
    version: str
    purl: str
    scope: str
    licence: str
    rule: str


@dataclass
class Result:
    violations: list[Finding] = field(default_factory=list)
    reviews: list[Finding] = field(default_factory=list)
    base_copyleft: list[Finding] = field(default_factory=list)
    components: int = 0


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        raise SystemExit(f"error: cannot read {path}: {err}") from err


def component_type(component: dict) -> str:
    for prop in component.get("properties", []):
        if prop.get("name") == "syft:package:type":
            return prop.get("value", "")
    purl = component.get("purl", "")
    if purl.startswith("pkg:"):
        return purl[4:].split("/", 1)[0]
    return ""


def licence_expression(component: dict) -> str:
    """Return one SPDX-like expression for the component, or UNKNOWN."""
    parts = []
    for entry in component.get("licenses", []):
        if "expression" in entry:
            parts.append(entry["expression"])
        elif "license" in entry:
            lic = entry["license"]
            parts.append(lic.get("id") or lic.get("name") or "")
    parts = [p.strip() for p in parts if p and p.strip()]
    if not parts:
        return UNKNOWN
    # Several license entries in CycloneDX mean all of them apply.
    return " AND ".join(f"({p})" if " " in p else p for p in parts)


def _matches(licence_id: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(licence_id, pat) for pat in patterns)


def _parse(tokens: list[str], patterns: list[str]) -> bool:
    """Evaluate whether an expression is forced into a denied licence.

    AND: denied if any side is denied (all terms apply).
    OR: denied only if every alternative is denied (we may choose).
    WITH: the exception does not change the base licence.
    """

    def expr(i: int) -> tuple[bool, int]:
        value, i = term(i)
        while i < len(tokens) and tokens[i] == "OR":
            right, i = term(i + 1)
            value = value and right
        return value, i

    def term(i: int) -> tuple[bool, int]:
        value, i = factor(i)
        while i < len(tokens) and tokens[i] == "AND":
            right, i = factor(i + 1)
            value = value or right
        return value, i

    def factor(i: int) -> tuple[bool, int]:
        if i >= len(tokens):
            return False, i
        if tokens[i] == "(":
            value, i = expr(i + 1)
            if i < len(tokens) and tokens[i] == ")":
                i += 1
            return value, i
        value = _matches(tokens[i], patterns)
        i += 1
        if i < len(tokens) and tokens[i] == "WITH":
            i += 2
        return value, i

    return expr(0)[0]


def is_denied(expression: str, patterns: list[str]) -> bool:
    if not patterns or expression == UNKNOWN:
        return False
    return _parse(_TOKEN.findall(expression), patterns)


def mentions(expression: str, patterns: list[str]) -> bool:
    return any(_matches(tok, patterns) for tok in _TOKEN.findall(expression))


def is_excepted(purl: str, policy: dict) -> bool:
    return any(
        purl.startswith(exc["purl_prefix"]) for exc in policy.get("exceptions", [])
    )


def _finding(path: Path, comp: dict, scope: str, licence: str, rule: str) -> Finding:
    return Finding(
        path.name,
        comp.get("name", "?"),
        comp.get("version", "?"),
        comp.get("purl", ""),
        scope,
        licence,
        rule,
    )


def check(sboms: list[Path], policy: dict) -> Result:
    base_types = set(policy.get("base_layer_types", []))
    result = Result()
    for path in sboms:
        bom = load_json(path)
        if bom.get("bomFormat") != "CycloneDX":
            raise SystemExit(f"error: {path} is not a CycloneDX SBOM")
        for comp in bom.get("components", []):
            if comp.get("type") in ("operating-system", "file"):
                continue
            result.components += 1
            purl = comp.get("purl", "")
            scope = "base" if component_type(comp) in base_types else "application"
            licence = licence_expression(comp)

            if is_excepted(purl, policy):
                continue
            if is_denied(licence, policy.get("deny_everywhere", [])):
                result.violations.append(
                    _finding(path, comp, scope, licence, "denied in any shipped image")
                )
            elif scope == "application":
                if licence == UNKNOWN and policy.get(
                    "require_known_licence_in_application", True
                ):
                    result.violations.append(
                        _finding(path, comp, scope, licence, "no licence found")
                    )
                elif is_denied(licence, policy.get("deny_in_application", [])):
                    result.violations.append(
                        _finding(
                            path, comp, scope, licence, "denied in application code"
                        )
                    )
                elif mentions(licence, policy.get("review_in_application", [])):
                    result.reviews.append(
                        _finding(path, comp, scope, licence, "weak copyleft: review")
                    )
            elif mentions(licence, ["GPL-*", "LGPL-*"]):
                result.base_copyleft.append(
                    _finding(path, comp, scope, licence, "base layer, allowed")
                )
    return result


def _table(findings: list[Finding]) -> list[str]:
    rows = ["| SBOM | Package | Version | Licence | Rule |", "|---|---|---|---|---|"]
    for f in findings:
        rows.append(f"| {f.sbom} | {f.name} | {f.version} | {f.licence} | {f.rule} |")
    return rows


def report(result: Result) -> str:
    status = "FAILED" if result.violations else "passed"
    lines = [
        f"## Licence policy {status}",
        "",
        f"Components checked: {result.components}. "
        f"Violations: {len(result.violations)}. "
        f"For review: {len(result.reviews)}. "
        f"Copyleft packages in the OS base layer (allowed): "
        f"{len(result.base_copyleft)}.",
    ]
    if result.violations:
        lines += ["", "### Violations", "", *_table(result.violations)]
    if result.reviews:
        lines += ["", "### For review (not blocking)", "", *_table(result.reviews)]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("sboms", type=Path, nargs="+")
    args = parser.parse_args(argv)
    try:
        result = check(args.sboms, load_json(args.policy))
    except SystemExit as err:
        print(err, file=sys.stderr)
        return 2
    text = report(result)
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(text)
    for f in result.violations:
        print(
            f"::error title=Licence policy::{f.name} {f.version} ({f.licence}): "
            f"{f.rule} [{f.sbom}]"
        )
    return 1 if result.violations else 0


if __name__ == "__main__":
    sys.exit(main())
