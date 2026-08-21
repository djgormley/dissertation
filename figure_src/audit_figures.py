#!/usr/bin/env python3
"""Audit dissertation figure reproducibility, typography, and visual contracts."""
from __future__ import annotations

import csv
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from .frozen_data import FrozenDataError, verify_frozen_data
except ImportError:  # direct-script fallback
    from frozen_data import FrozenDataError, verify_frozen_data

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).resolve().parent / "figure_manifest.csv"
REPORT = ROOT / "FIGURE_AUDIT_REPORT.md"
TEX_FILES = [ROOT / "dissertation.tex", *sorted((ROOT / "chapters").glob("*.tex"))]
RASTER_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
EXPECTED_PALETTE = {
    "ppMeasured": "0062A3",
    "ppModel": "7F6310",
    "ppConditional": "6A724F",
    "ppFailure": "8D4638",
    "ppPending": "988E8B",
}
PYTHON_PALETTE = {
    "MEASURED": "0062A3",
    "MODEL": "7F6310",
    "CONDITIONAL": "6A724F",
    "FAILURE": "8D4638",
    "PENDING": "988E8B",
}
FIGURE_MANIFEST_FIELDS = (
    "artifact",
    "kind",
    "active",
    "chapter",
    "editable_source",
    "data_dependencies",
    "provenance",
    "notes",
    "font",
    "conventions",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(*args: str) -> str:
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        raise RuntimeError(
            f"command failed ({proc.returncode}): {' '.join(args)}\n{proc.stdout}\n{proc.stderr}"
        )
    return proc.stdout


def read_manifest() -> list[dict[str, str]]:
    with MANIFEST.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != FIGURE_MANIFEST_FIELDS:
            raise RuntimeError(
                "figure_manifest.csv header does not match the required schema"
            )
        rows = list(reader)
    for line_number, row in enumerate(rows, start=2):
        if None in row or any(value is None for value in row.values()):
            raise RuntimeError(
                f"figure_manifest.csv:{line_number}: wrong number of CSV fields"
            )
    return rows


def tex_inventory() -> tuple[dict[str, str], set[str], list[str]]:
    graphics: dict[str, str] = {}
    tikz_inputs: set[str] = set()
    inline: list[str] = []
    graphic_re = re.compile(r"\\includegraphics(?:\[([^\]]*)\])?\{([^}]+)\}")
    input_re = re.compile(r"\\input\{(figure_src/tikz/[^}]+\.tikz)\}")
    for path in TEX_FILES:
        text = path.read_text(encoding="utf-8")
        for match in graphic_re.finditer(text):
            options, artifact = match.group(1) or "", match.group(2)
            graphics[artifact] = options
        for match in input_re.finditer(text):
            rel = match.group(1)
            if not rel.endswith("figure_styles.tikz"):
                tikz_inputs.add(rel)
        if r"\begin{tikzpicture}" in text:
            inline.append(path.relative_to(ROOT).as_posix())
    return graphics, tikz_inputs, inline


def font_audit(path: Path) -> tuple[list[str], list[str]]:
    text = run("pdffonts", str(path))
    fonts: list[str] = []
    errors: list[str] = []
    lines = text.splitlines()[2:]
    for line in lines:
        if not line.strip():
            continue
        tokens = line.split()
        if len(tokens) < 9:
            errors.append(f"could not parse pdffonts row: {line}")
            continue
        name = tokens[0]
        embedded = tokens[-5]
        fonts.append(name)
        if embedded.lower() != "yes":
            errors.append(f"font is not embedded: {name}")
        if "Type 3" in line:
            errors.append(f"Type 3 font present: {name}")
        if "DejaVu" in name:
            errors.append(f"DejaVu substitution present: {name}")
        if not (name.startswith("LM") or "LatinModern" in name):
            errors.append(f"non-Latin-Modern font present: {name}")
    if not fonts:
        errors.append("no fonts reported by pdffonts")
    return sorted(set(fonts)), errors


def vector_audit(path: Path) -> list[str]:
    text = run("pdfimages", "-list", str(path))
    rows = [line for line in text.splitlines()[2:] if line.strip()]
    return [f"embedded raster image object: {line.strip()}" for line in rows]


def page_count(path: Path) -> int:
    text = run("pdfinfo", str(path))
    m = re.search(r"^Pages:\s+(\d+)\s*$", text, re.MULTILINE)
    if not m:
        raise RuntimeError(f"could not read page count for {path}")
    return int(m.group(1))


def palette_audit() -> list[str]:
    errors: list[str] = []
    tex = (ROOT / "dissertation.tex").read_text(encoding="utf-8")
    py = (ROOT / "figure_src/style.py").read_text(encoding="utf-8")
    tikz = (ROOT / "figure_src/tikz/figure_styles.tikz").read_text(encoding="utf-8")
    for name, value in EXPECTED_PALETTE.items():
        if not re.search(rf"\\definecolor\{{{re.escape(name)}\}}\{{HTML\}}\{{{value}\}}", tex):
            errors.append(f"missing or changed LaTeX palette value: {name}={value}")
        if name not in tikz:
            errors.append(f"TikZ style file does not use {name}")
    for name, value in PYTHON_PALETTE.items():
        if not re.search(rf"^{name}\s*=\s*[\"']#{value}[\"']", py, re.MULTILINE):
            errors.append(f"missing or changed Python palette value: {name}=#{value}")
    return errors


def main() -> int:
    required_tools = ("pdffonts", "pdfimages", "pdfinfo")
    errors: list[str] = []
    for tool in required_tools:
        if not shutil.which(tool):
            errors.append(f"required audit command is unavailable: {tool}")

    frozen_manifest = None
    try:
        frozen_manifest = verify_frozen_data()
    except FrozenDataError as exc:
        errors.append(f"frozen data audit failed: {exc}")

    rows = read_manifest()
    by_artifact = {row["artifact"]: row for row in rows}
    if len(by_artifact) != len(rows):
        errors.append("duplicate artifact in figure_manifest.csv")

    graphics, tikz_inputs, inline = tex_inventory()
    if inline:
        errors.append("inline TikZ remains in: " + ", ".join(inline))

    frozen_prefix = "figure_src/data/frozen_export/v1/"
    frozen_dependencies = {
        dep
        for row in rows
        for dep in row["data_dependencies"].split(";")
        if dep.startswith(frozen_prefix)
    }
    if frozen_manifest is not None:
        frozen_inventory = {
            frozen_prefix + record["path"]
            for record in frozen_manifest["artifacts"]
        }
        if frozen_dependencies != frozen_inventory:
            errors.append(
                "frozen data inventory differs from figure dependencies: "
                f"manifest-only={sorted(frozen_inventory-frozen_dependencies)}, "
                f"figure-only={sorted(frozen_dependencies-frozen_inventory)}"
            )

    active_manifest = {row["artifact"] for row in rows if row["active"] == "yes"}
    active_pdf_manifest = {a for a in active_manifest if a.endswith(".pdf")}
    active_tikz_manifest = {a for a in active_manifest if a.endswith(".tikz")}
    graphic_set = set(graphics)
    if graphic_set != active_pdf_manifest:
        errors.append(
            "active PDF inventory differs from TeX includes: "
            f"manifest-only={sorted(active_pdf_manifest-graphic_set)}, "
            f"tex-only={sorted(graphic_set-active_pdf_manifest)}"
        )
    if tikz_inputs != active_tikz_manifest:
        errors.append(
            "active TikZ inventory differs from chapter inputs: "
            f"manifest-only={sorted(active_tikz_manifest-tikz_inputs)}, "
            f"tex-only={sorted(tikz_inputs-active_tikz_manifest)}"
        )

    for artifact, options in graphics.items():
        if Path(artifact).suffix.lower() in RASTER_EXTENSIONS:
            errors.append(f"active raster include is not allowed: {artifact}")
        if r"width=0.98\linewidth" not in options:
            errors.append(f"active external figure does not use the common 0.98-linewidth convention: {artifact}")

    generated_pdf_set = {p.relative_to(ROOT).as_posix() for p in (ROOT / "figs").glob("*.pdf")}
    manifest_pdf_set = {row["artifact"] for row in rows if row["kind"] == "pdf"}
    if generated_pdf_set != manifest_pdf_set:
        errors.append(
            "figs/ PDF inventory differs from manifest: "
            f"manifest-only={sorted(manifest_pdf_set-generated_pdf_set)}, "
            f"directory-only={sorted(generated_pdf_set-manifest_pdf_set)}"
        )

    errors.extend(palette_audit())

    report_rows: list[dict[str, str]] = []
    if not errors or all(shutil.which(t) for t in required_tools):
        for row in rows:
            artifact = ROOT / row["artifact"]
            row_errors: list[str] = []
            if not artifact.is_file():
                row_errors.append("artifact missing")
            source_rel = row["editable_source"].split("::", 1)[0]
            if source_rel.startswith("WVURAIL/"):
                pass  # rendered in the owning repository; PDF is vendored
            else:
                source = ROOT / source_rel
                if not source.is_file():
                    row_errors.append(f"editable source missing: {source_rel}")
            deps = [d for d in row["data_dependencies"].split(";")
                    if d and d not in ("none", "external")]
            for dep in deps:
                if not (ROOT / dep).is_file():
                    row_errors.append(f"data dependency missing: {dep}")
            fonts: list[str] = []
            if artifact.is_file() and row["kind"] == "pdf" and all(shutil.which(t) for t in required_tools):
                if page_count(artifact) != 1:
                    row_errors.append("generated figure is not exactly one PDF page")
                fonts, font_errors = font_audit(artifact)
                row_errors.extend(font_errors)
                row_errors.extend(vector_audit(artifact))
            errors.extend(f"{row['artifact']}: {e}" for e in row_errors)
            report_rows.append({
                "artifact": row["artifact"],
                "active": row["active"],
                "source": row["editable_source"],
                "provenance": row["provenance"],
                "fonts": ", ".join(fonts) if fonts else "inherits dissertation (TikZ)",
                "sha256": sha256(artifact) if artifact.is_file() else "MISSING",
                "status": "PASS" if not row_errors else "FAIL",
            })

    status = "PASS" if not errors else "FAIL"
    lines = [
        "# Figure audit report",
        "",
        f"**Overall status: {status}**",
        "",
        f"- Manifest artifacts: {len(rows)}",
        f"- Active external PDFs: {len(active_pdf_manifest)}",
        f"- Active named TikZ figures: {len(active_tikz_manifest)}",
        f"- Generated but unused source-backed PDFs: {len(manifest_pdf_set-active_pdf_manifest)}",
        f"- Frozen data tables: {len(frozen_manifest['artifacts']) if frozen_manifest else 0}",
        f"- Frozen tables awaiting authoritative replacement: {sum(bool(a.get('replacement_required')) for a in frozen_manifest['artifacts']) if frozen_manifest else 0}",
        "- Production font contract: embedded Latin Modern; no Type 3 or DejaVu substitution",
        "- Active external format contract: vector PDF only",
        "- Inclusion-size contract: 0.98 of the dissertation text width",
        "",
    ]
    if errors:
        lines += ["## Failures", ""] + [f"- {e}" for e in errors] + [""]
    lines += [
        "## Artifact inventory",
        "",
        "| Artifact | Active | Source | Provenance | Font audit | SHA-256 | Status |",
        "|---|---:|---|---|---|---|---:|",
    ]
    for r in report_rows:
        fonts = r["fonts"].replace("|", "\\|")
        lines.append(
            f"| `{r['artifact']}` | {r['active']} | `{r['source']}` | "
            f"{r['provenance']} | {fonts} | `{r['sha256']}` | {r['status']} |"
        )
    lines += [
        "",
        "## Scope",
        "",
        "This report verifies that every included visual is source-backed, that all listed dependencies are present, "
        "that the frozen-data manifest matches every CSV byte and row count, that the active external figures are "
        "one-page vector PDFs, that their fonts are embedded Latin Modern fonts, and that the Python/TikZ semantic "
        "palettes agree. It does not replace scientific validation of the values in the input tables; authority and "
        "replacement status are recorded in `figure_src/data/frozen_export/v1/frozen_data_manifest.json`.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{status}: wrote {REPORT}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
