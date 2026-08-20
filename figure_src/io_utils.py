"""Paths and small CSV helpers used by the local figure generators."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figs"
DATA = Path(__file__).resolve().parent / "data" / "frozen_export" / "v1"


def read_csv(name: str):
    with (DATA / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def columns(rows, *names):
    import numpy as np
    return tuple(np.asarray([float(r[n]) for r in rows]) for n in names)
