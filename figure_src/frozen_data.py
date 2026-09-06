"""Validation helpers for the dissertation's frozen tabular data interface."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data" / "frozen_export" / "v1"
MANIFEST_PATH = DATA_DIR / "frozen_data_manifest.json"
SCHEMA = {"name": "pilot-proxy-dissertation-frozen-data", "version": 1}


class FrozenDataError(RuntimeError):
    """Raised when a frozen dissertation data table or manifest is invalid."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FrozenDataError(f"frozen data manifest is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FrozenDataError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise FrozenDataError(f"frozen data manifest root is not an object: {path}")
    return manifest


def verify_frozen_data(
    data_dir: Path = DATA_DIR,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Verify manifest schema, paths, hashes, and row counts."""
    data_dir = data_dir.resolve()
    manifest_path = manifest_path or data_dir / "frozen_data_manifest.json"
    manifest = load_manifest(manifest_path)
    if manifest.get("schema") != SCHEMA:
        raise FrozenDataError(
            f"unsupported frozen data schema: {manifest.get('schema')!r}"
        )
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise FrozenDataError("frozen data manifest artifacts must be a non-empty list")
    seen: set[str] = set()
    for record in artifacts:
        if not isinstance(record, dict):
            raise FrozenDataError("frozen data manifest contains a non-object record")
        relative = str(record.get("path", ""))
        candidate = Path(relative)
        if not relative or candidate.is_absolute() or ".." in candidate.parts:
            raise FrozenDataError(f"unsafe frozen-data path: {relative!r}")
        if relative in seen:
            raise FrozenDataError(f"duplicate frozen-data path: {relative}")
        seen.add(relative)
        path = data_dir / relative
        if not path.is_file():
            raise FrozenDataError(f"frozen data table is missing: {path}")
        actual_hash = sha256(path)
        if record.get("sha256") != actual_hash:
            raise FrozenDataError(
                f"SHA-256 mismatch for {relative}: expected {record.get('sha256')}, "
                f"got {actual_hash}"
            )
        actual_rows = row_count(path)
        if int(record.get("rows", -1)) != actual_rows:
            raise FrozenDataError(
                f"row-count mismatch for {relative}: expected {record.get('rows')}, "
                f"got {actual_rows}"
            )
        if not record.get("owner") or not record.get("authority"):
            raise FrozenDataError(f"missing ownership/authority metadata for {relative}")
        if not isinstance(record.get("replacement_required"), bool):
            raise FrozenDataError(f"replacement_required must be boolean for {relative}")
    csv_files = {path.name for path in data_dir.glob("*.csv")}
    if csv_files != seen:
        raise FrozenDataError(
            "frozen-data CSV inventory differs from manifest: "
            f"manifest-only={sorted(seen-csv_files)}, directory-only={sorted(csv_files-seen)}"
        )
    return manifest
