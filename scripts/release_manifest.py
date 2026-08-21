#!/usr/bin/env python3
"""Regenerate or verify the dissertation release-bundle manifest.

The release boundary is every Git-tracked file in this repository except
``MANIFEST.sha256`` itself. Untracked and ignored build scratch is not part of
the bundle. The self-exclusion avoids an impossible self-referential digest.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_RELATIVE = "MANIFEST.sha256"
MANIFEST = ROOT / MANIFEST_RELATIVE
SHA256_RE = re.compile(r"[0-9a-f]{64}")
VERIFIER_RELATIVE = Path(__file__).resolve().relative_to(ROOT).as_posix()


def _tracked_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z"],
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(
            "release-manifest verification requires a Git checkout"
        ) from exc
    paths = [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]
    # Bootstrap this verifier into the boundary while it is still an uncommitted
    # addition. Once committed, the set insertion is naturally idempotent.
    paths.append(VERIFIER_RELATIVE)
    return sorted(set(paths) - {MANIFEST_RELATIVE})


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _parse_manifest() -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    entries: dict[str, str] = {}
    try:
        lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return {}, [f"missing release manifest: {MANIFEST_RELATIVE}"]

    for line_number, line in enumerate(lines, start=1):
        if len(line) < 67 or line[64:66] != "  ":
            errors.append(
                f"{MANIFEST_RELATIVE}:{line_number}: expected '<sha256>  <path>'"
            )
            continue
        digest = line[:64]
        relative = line[66:]
        path = PurePosixPath(relative)
        if not SHA256_RE.fullmatch(digest):
            errors.append(
                f"{MANIFEST_RELATIVE}:{line_number}: invalid SHA-256 digest"
            )
        if not relative or path.is_absolute() or ".." in path.parts:
            errors.append(
                f"{MANIFEST_RELATIVE}:{line_number}: unsafe relative path {relative!r}"
            )
            continue
        if relative == MANIFEST_RELATIVE:
            errors.append(
                f"{MANIFEST_RELATIVE}:{line_number}: manifest must exclude itself"
            )
            continue
        if relative in entries:
            errors.append(
                f"{MANIFEST_RELATIVE}:{line_number}: duplicate path {relative!r}"
            )
            continue
        entries[relative] = digest
    return entries, errors


def write_manifest() -> None:
    tracked = _tracked_files()
    lines = [f"{_sha256(ROOT / relative)}  {relative}\n" for relative in tracked]
    temporary = MANIFEST.with_suffix(".sha256.tmp")
    temporary.write_text("".join(lines), encoding="utf-8", newline="\n")
    temporary.replace(MANIFEST)
    print(f"Wrote {MANIFEST_RELATIVE} for {len(tracked)} tracked bundle files")


def verify_manifest() -> int:
    tracked = set(_tracked_files())
    entries, errors = _parse_manifest()
    listed = set(entries)
    for relative in sorted(tracked - listed):
        errors.append(f"tracked bundle file missing from manifest: {relative}")
    for relative in sorted(listed - tracked):
        errors.append(f"manifest path is not a tracked bundle file: {relative}")

    for relative in sorted(tracked & listed):
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"tracked bundle file is missing: {relative}")
            continue
        actual = _sha256(path)
        if actual != entries[relative]:
            errors.append(
                f"SHA-256 mismatch for {relative}: "
                f"expected {entries[relative]}, got {actual}"
            )

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"Release manifest verification failed with {len(errors)} error(s)")
        return 1
    print(f"Verified {MANIFEST_RELATIVE}: {len(tracked)} tracked bundle files")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="regenerate the manifest before verifying it",
    )
    args = parser.parse_args(argv)
    try:
        if args.write:
            write_manifest()
        return verify_manifest()
    except RuntimeError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
