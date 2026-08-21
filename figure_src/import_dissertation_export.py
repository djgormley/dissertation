#!/usr/bin/env python3
"""Import a verified PilotProxy data export into the frozen dissertation data set."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Sequence

from .frozen_data import DATA_DIR, FrozenDataError, row_count, sha256, verify_frozen_data

UPSTREAM_SCHEMA = {"name": "pilot-proxy-dissertation-export", "version": 1}
UPSTREAM_REPOSITORY = "WVURAIL/pilot-proxy"
IMMUTABLE_COMMIT_RE = re.compile(r"[0-9a-f]{40}")
COMPLETE_SCOPE = (
    "PilotProxy dissertation-export v1 tabular interface only; this flag does not "
    "describe all-23-channel CANFAR archive coverage"
)


class ExportImportError(RuntimeError):
    """Raised when an upstream export cannot be imported safely."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ExportImportError(f"upstream export manifest is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ExportImportError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ExportImportError(f"JSON root must be an object: {path}")
    return value


def verify_upstream(export_dir: Path, *, require_complete: bool = False) -> dict[str, Any]:
    export_dir = export_dir.resolve()
    manifest = _load_json(export_dir / "export_manifest.json")
    if manifest.get("schema") != UPSTREAM_SCHEMA:
        raise ExportImportError(f"unsupported upstream export schema: {manifest.get('schema')!r}")
    source = manifest.get("source")
    if not isinstance(source, dict):
        raise ExportImportError("upstream source record must be an object")
    repository = source.get("repository")
    if repository != UPSTREAM_REPOSITORY:
        raise ExportImportError(
            f"upstream source repository must use canonical slug {UPSTREAM_REPOSITORY!r}"
        )
    commit = source.get("commit")
    if not isinstance(commit, str) or not IMMUTABLE_COMMIT_RE.fullmatch(commit):
        raise ExportImportError(
            "upstream source commit must be a full 40-character lowercase Git SHA"
        )
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ExportImportError("upstream artifacts must be a list")
    complete = True
    seen: set[str] = set()
    for record in artifacts:
        if not isinstance(record, dict):
            raise ExportImportError("upstream manifest contains a non-object artifact")
        relative = str(record.get("path", ""))
        candidate = Path(relative)
        if not relative or candidate.is_absolute() or ".." in candidate.parts:
            raise ExportImportError(f"unsafe upstream artifact path: {relative!r}")
        if relative in seen:
            raise ExportImportError(f"duplicate upstream artifact path: {relative}")
        seen.add(relative)
        status = record.get("status")
        if status == "pending":
            complete = False
            continue
        if status != "available":
            raise ExportImportError(f"unknown upstream status for {relative}: {status!r}")
        path = export_dir / relative
        if not path.is_file():
            raise ExportImportError(f"available upstream artifact is missing: {path}")
        if sha256(path) != record.get("sha256"):
            raise ExportImportError(f"SHA-256 mismatch in upstream export: {relative}")
        if row_count(path) != int(record.get("rows", -1)):
            raise ExportImportError(f"row-count mismatch in upstream export: {relative}")
    if bool(manifest.get("complete")) != complete:
        raise ExportImportError("upstream complete flag disagrees with artifact statuses")
    if require_complete and not complete:
        pending = [r["path"] for r in artifacts if r.get("status") == "pending"]
        raise ExportImportError("upstream export is partial: " + ", ".join(pending))
    return manifest


def import_export(
    export_dir: Path,
    *,
    data_dir: Path = DATA_DIR,
    require_complete: bool = False,
    dry_run: bool = False,
) -> list[str]:
    """Import all matching available tables and return their relative paths."""
    export_dir = export_dir.resolve()
    data_dir = data_dir.resolve()
    upstream = verify_upstream(export_dir, require_complete=require_complete)
    current = verify_frozen_data(data_dir)
    records = {record["path"]: dict(record) for record in current["artifacts"]}
    available = [
        record for record in upstream["artifacts"]
        if record.get("status") == "available" and record.get("path") in records
    ]
    if not available:
        raise ExportImportError("upstream export contains no table recognized by this dissertation")
    imported = [str(record["path"]) for record in available]
    if dry_run:
        return imported

    parent = data_dir.parent
    temp = Path(tempfile.mkdtemp(prefix=f".{data_dir.name}.", dir=parent))
    shutil.rmtree(temp)
    shutil.copytree(data_dir, temp)
    try:
        commit = upstream.get("source", {}).get("commit", "unknown")
        repository = upstream.get("source", {}).get("repository", "WVURAIL/pilot-proxy")
        for incoming in available:
            relative = str(incoming["path"])
            source = export_dir / relative
            destination = temp / relative
            shutil.copy2(source, destination)
            record = records[relative]
            record.update(
                {
                    "status": "frozen",
                    "owner": incoming.get("owner", record.get("owner")),
                    "authority": incoming.get("authority", record.get("authority")),
                    "description": incoming.get("description", record.get("description")),
                    "rows": int(incoming["rows"]),
                    "sha256": str(incoming["sha256"]),
                    "source_kind": "pilot-proxy-export",
                    "authoritative_for_draft": True,
                    "replacement_required": False,
                    "upstream": f"{repository}@{commit}: {relative}",
                }
            )
            records[relative] = record

        updated = dict(current)
        updated["artifacts"] = [records[name] for name in sorted(records)]
        updated.setdefault("upstream_exports", {})["pilot_proxy"] = {
            "schema": upstream["schema"],
            "repository": repository,
            "commit": commit,
            "summary_snapshot_id": upstream.get("source", {}).get(
                "summary_snapshot_id", "unknown"
            ),
            "complete": bool(upstream.get("complete")),
            "complete_scope": COMPLETE_SCOPE,
        }
        (temp / "frozen_data_manifest.json").write_text(
            json.dumps(updated, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        import_record = {
            "source_export": f"{repository}@{commit}",
            "source_export_manifest_sha256": sha256(
                export_dir / "export_manifest.json"
            ),
            "source_repository": repository,
            "source_commit": commit,
            "source_summary_snapshot_id": upstream.get("source", {}).get(
                "summary_snapshot_id", "unknown"
            ),
            "source_complete": bool(upstream.get("complete")),
            "imported_artifacts": imported,
        }
        (temp / "last_import.json").write_text(
            json.dumps(import_record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        verify_frozen_data(temp, temp / "frozen_data_manifest.json")
        backup = data_dir.with_name(data_dir.name + ".previous")
        if backup.exists():
            shutil.rmtree(backup)
        os.replace(data_dir, backup)
        try:
            os.replace(temp, data_dir)
        except Exception:
            os.replace(backup, data_dir)
            raise
        shutil.rmtree(backup)
        return imported
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export_dir", type=Path, help="PilotProxy dissertation export directory")
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        imported = import_export(
            args.export_dir,
            require_complete=args.require_complete,
            dry_run=args.dry_run,
        )
    except (ExportImportError, FrozenDataError) as exc:
        parser.exit(2, f"error: {exc}\n")
    action = "Would import" if args.dry_run else "Imported"
    print(f"{action} {len(imported)} table(s):")
    for relative in imported:
        print(f"  {relative}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
