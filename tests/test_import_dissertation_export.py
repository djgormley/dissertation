"""Regression tests for portable dissertation-export import provenance."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from figure_src.frozen_data import SCHEMA, sha256
from figure_src.import_dissertation_export import (
    UPSTREAM_SCHEMA,
    UPSTREAM_REPOSITORY,
    ExportImportError,
    import_export,
    verify_upstream,
)


class ImportDissertationExportTest(unittest.TestCase):
    def _fixture(
        self,
        root: Path,
        *,
        commit: str,
        repository: str = UPSTREAM_REPOSITORY,
    ) -> tuple[Path, Path]:
        data_dir = root / "frozen" / "v1"
        export_dir = root / "machine-specific" / "pilot-export"
        data_dir.mkdir(parents=True)
        export_dir.mkdir(parents=True)

        relative = "table.csv"
        frozen_table = data_dir / relative
        frozen_table.write_text("value\nold\n", encoding="utf-8", newline="\n")
        frozen_manifest = {
            "schema": SCHEMA,
            "artifacts": [
                {
                    "path": relative,
                    "rows": 1,
                    "sha256": sha256(frozen_table),
                    "owner": "dissertation",
                    "authority": "test fixture",
                    "replacement_required": False,
                }
            ],
        }
        (data_dir / "frozen_data_manifest.json").write_text(
            json.dumps(frozen_manifest), encoding="utf-8", newline="\n"
        )

        exported_table = export_dir / relative
        exported_table.write_text("value\nnew\n", encoding="utf-8", newline="\n")
        export_manifest = {
            "schema": UPSTREAM_SCHEMA,
            "source": {
                "repository": repository,
                "commit": commit,
                "summary_snapshot_id": "dissertation-summary-v3",
            },
            "artifacts": [
                {
                    "path": relative,
                    "status": "available",
                    "rows": 1,
                    "sha256": sha256(exported_table),
                    "owner": "pilot-proxy",
                    "authority": "test fixture",
                    "description": "test table",
                }
            ],
            "complete": True,
        }
        (export_dir / "export_manifest.json").write_text(
            json.dumps(export_manifest), encoding="utf-8", newline="\n"
        )
        return data_dir, export_dir

    def test_last_import_uses_portable_source_identity(self) -> None:
        commit = "a" * 40
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            data_dir, export_dir = self._fixture(root, commit=commit)
            export_manifest_hash = sha256(export_dir / "export_manifest.json")

            import_export(export_dir, data_dir=data_dir)

            record_text = (data_dir / "last_import.json").read_text(encoding="utf-8")
            record = json.loads(record_text)
            self.assertEqual(record["source_export"], f"WVURAIL/pilot-proxy@{commit}")
            self.assertEqual(
                record["source_export_manifest_sha256"], export_manifest_hash
            )
            self.assertEqual(
                record["source_summary_snapshot_id"], "dissertation-summary-v3"
            )
            self.assertNotIn(str(root), record_text)

    def test_nonimmutable_source_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, export_dir = self._fixture(
                Path(temporary), commit="base=deadbeef;source=working-tree"
            )
            with self.assertRaisesRegex(
                ExportImportError, "full 40-character lowercase Git SHA"
            ):
                verify_upstream(export_dir)

    def test_machine_path_source_repository_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, export_dir = self._fixture(
                root, commit="a" * 40, repository=str(root / "pilot-proxy")
            )
            with self.assertRaisesRegex(ExportImportError, "canonical slug"):
                verify_upstream(export_dir)


if __name__ == "__main__":
    unittest.main()
