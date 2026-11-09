import json
import tempfile
import unittest
from pathlib import Path

from tools.licence import licence_check as lc

POLICY = {
    "base_layer_types": ["deb", "binary"],
    "deny_everywhere": ["AGPL-*"],
    "deny_in_application": ["GPL-*", "AGPL-*"],
    "review_in_application": ["LGPL-*", "MPL-*"],
    "require_known_licence_in_application": True,
    "exceptions": [{"purl_prefix": "pkg:pypi/allowed-gpl@", "reason": "test"}],
}


def comp(name, ptype, licences=None, expression=None):
    entry = {
        "type": "library",
        "name": name,
        "version": "1.0",
        "purl": f"pkg:{ptype}/{name}@1.0",
        "properties": [{"name": "syft:package:type", "value": ptype}],
    }
    if expression:
        entry["licenses"] = [{"expression": expression}]
    elif licences:
        entry["licenses"] = [{"license": {"id": lic}} for lic in licences]
    return entry


def run(components):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "sbom.cdx.json"
        path.write_text(
            json.dumps({"bomFormat": "CycloneDX", "components": components})
        )
        return lc.check([path], POLICY)


class ExpressionTest(unittest.TestCase):
    def test_or_needs_every_option_denied(self):
        self.assertFalse(lc.is_denied("MIT OR GPL-3.0-only", ["GPL-*"]))
        self.assertTrue(lc.is_denied("GPL-2.0-only OR GPL-3.0-only", ["GPL-*"]))

    def test_and_denied_if_any_part_denied(self):
        self.assertTrue(lc.is_denied("MIT AND GPL-3.0-only", ["GPL-*"]))

    def test_with_exception_and_parentheses(self):
        expr = "(MIT OR Apache-2.0) AND GPL-2.0-only WITH Classpath-exception-2.0"
        self.assertTrue(lc.is_denied(expr, ["GPL-*"]))
        self.assertFalse(
            lc.is_denied("(MIT OR GPL-3.0-only) AND BSD-3-Clause", ["GPL-*"])
        )

    def test_lgpl_is_not_matched_by_gpl_pattern(self):
        self.assertFalse(lc.is_denied("LGPL-2.1-only", ["GPL-*"]))


class PolicyTest(unittest.TestCase):
    def test_gpl_in_base_layer_is_allowed_but_reported(self):
        result = run([comp("bash", "deb", ["GPL-3.0-or-later"])])
        self.assertEqual(result.violations, [])
        self.assertEqual(len(result.base_copyleft), 1)

    def test_agpl_fails_even_in_base_layer(self):
        result = run([comp("ghostscript", "deb", ["AGPL-3.0-or-later"])])
        self.assertEqual(len(result.violations), 1)

    def test_gpl_in_application_fails(self):
        result = run([comp("somelib", "pypi", ["GPL-3.0-only"])])
        self.assertEqual(result.violations[0].rule, "denied in application code")

    def test_unknown_licence_in_application_fails(self):
        result = run([comp("mystery", "pypi")])
        self.assertEqual(result.violations[0].rule, "no licence found")

    def test_permissive_application_passes(self):
        result = run([comp("protobuf", "pypi", ["BSD-3-Clause"])])
        self.assertEqual(result.violations, [])
        self.assertEqual(result.reviews, [])

    def test_weak_copyleft_is_review_not_failure(self):
        result = run([comp("certifi", "pypi", expression="MPL-2.0")])
        self.assertEqual(result.violations, [])
        self.assertEqual(len(result.reviews), 1)

    def test_exception_skips_package(self):
        result = run([comp("allowed-gpl", "pypi", ["GPL-3.0-only"])])
        self.assertEqual(result.violations, [])


class MainTest(unittest.TestCase):
    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = Path(tmp) / "policy.json"
            policy.write_text(json.dumps(POLICY))
            good = Path(tmp) / "good.cdx.json"
            good.write_text(
                json.dumps(
                    {
                        "bomFormat": "CycloneDX",
                        "components": [comp("protobuf", "pypi", ["BSD-3-Clause"])],
                    }
                )
            )
            bad = Path(tmp) / "bad.cdx.json"
            bad.write_text(
                json.dumps(
                    {
                        "bomFormat": "CycloneDX",
                        "components": [comp("somelib", "pypi", ["GPL-3.0-only"])],
                    }
                )
            )
            spdx = Path(tmp) / "x.spdx.json"
            spdx.write_text(json.dumps({"spdxVersion": "SPDX-2.3"}))
            self.assertEqual(lc.main(["--policy", str(policy), str(good)]), 0)
            self.assertEqual(lc.main(["--policy", str(policy), str(bad)]), 1)
            self.assertEqual(lc.main(["--policy", str(policy), str(spdx)]), 2)


if __name__ == "__main__":
    unittest.main()
