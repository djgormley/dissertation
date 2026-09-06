"""Regression tests for the release-bundle manifest boundary."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import release_manifest


class ReleaseManifestTest(unittest.TestCase):
    def test_manifest_excludes_itself_and_bootstraps_verifier(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            verifier = root / "scripts" / "release_manifest.py"
            verifier.parent.mkdir()
            verifier.write_text("# test verifier\n", encoding="utf-8", newline="\n")
            (root / "tracked.txt").write_text(
                "tracked\n", encoding="utf-8", newline="\n"
            )
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "core.autocrlf=false",
                    "-C",
                    str(root),
                    "add",
                    "tracked.txt",
                ],
                check=True,
            )

            manifest = root / "MANIFEST.sha256"
            with patch.multiple(
                release_manifest,
                ROOT=root,
                MANIFEST=manifest,
                VERIFIER_RELATIVE="scripts/release_manifest.py",
            ):
                release_manifest.write_manifest()
                self.assertEqual(release_manifest.verify_manifest(), 0)

            listed = {
                line.split("  ", 1)[1]
                for line in manifest.read_text(encoding="utf-8").splitlines()
            }
            self.assertEqual(
                listed, {"scripts/release_manifest.py", "tracked.txt"}
            )
            self.assertNotIn("MANIFEST.sha256", listed)


if __name__ == "__main__":
    unittest.main()
