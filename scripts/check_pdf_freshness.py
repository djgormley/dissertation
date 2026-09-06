#!/usr/bin/env python3
"""Regenerate or verify the digest binding ``dissertation.pdf`` to its sources.

``MANIFEST.sha256`` proves that every tracked file matches its recorded digest,
but it cannot notice that the recorded ``dissertation.pdf`` was built from an
older revision of the LaTeX sources: refreshing the manifest against a stale PDF
produces a self-consistent bundle that CI happily accepts. That is exactly how a
two-commit source drift survived review once already.

This checker closes that gap without a TeX toolchain. ``make manifest`` rebuilds
the document and then records a single digest over every input the PDF is built
from. CI recomputes that digest and fails when the sources have moved but the
PDF has not, which is the only failure ``MANIFEST.sha256`` structurally cannot
see.

The digest deliberately covers *inputs only*. It says nothing about whether the
PDF bytes are reproducible on a different TeX Live; that is the manifest's job.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
DIGEST_RELATIVE = ".pdf-inputs-digest"
DIGEST_PATH = ROOT / DIGEST_RELATIVE

# Every path whose content can change a glyph in dissertation.pdf. Figures are
# included because the LaTeX run embeds them verbatim.
INPUT_GLOBS: tuple[str, ...] = (
    "dissertation.tex",
    "chapters/*.tex",
    "figs/**/*.pdf",
    "figure_src/tikz/*.tikz",
)


def _input_paths() -> list[Path]:
    seen: set[Path] = set()
    for pattern in INPUT_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file():
                seen.add(path)
    if not seen:
        raise RuntimeError("no dissertation build inputs matched; wrong root?")
    return sorted(seen)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _inputs_digest(paths: Iterable[Path]) -> str:
    combined = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        combined.update(f"{relative}\0{_sha256(path)}\0".encode("utf-8"))
    return combined.hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="record the current inputs digest (run only just after a rebuild)",
    )
    args = parser.parse_args(argv)

    paths = _input_paths()
    digest = _inputs_digest(paths)

    if args.write:
        DIGEST_PATH.write_text(digest + "\n", encoding="utf-8")
        print(f"Wrote {DIGEST_RELATIVE} over {len(paths)} build inputs")
        return 0

    if not DIGEST_PATH.exists():
        print(
            f"FAIL: {DIGEST_RELATIVE} is missing; run 'make manifest' to bind "
            "dissertation.pdf to its sources"
        )
        return 1

    recorded = DIGEST_PATH.read_text(encoding="utf-8").strip()
    if recorded != digest:
        print(
            "FAIL: dissertation.pdf is stale with respect to its sources.\n"
            f"  recorded inputs digest: {recorded}\n"
            f"  current  inputs digest: {digest}\n"
            "  The LaTeX sources or figures changed after the committed PDF was\n"
            "  built. Run 'make manifest' to rebuild the document and refresh\n"
            "  both the manifest and this digest."
        )
        return 1

    print(f"Verified dissertation.pdf freshness over {len(paths)} build inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
