#!/usr/bin/env python3
"""Regenerate every external dissertation figure.

Run from the dissertation root:

    python3 -m figure_src.generate_all

The command intentionally requires a working LaTeX installation so all figure
text uses Latin Modern, exactly like the dissertation body.
"""
from __future__ import annotations
from pathlib import Path

from . import style
from . import intro_figures, broadcast_figures, detector_figures, framework_figures, forecast_figures
from .io_utils import OUT

EXPECTED = {
    "fig_claim_chain.pdf", "fig_intro_soundwave.pdf", "fig_intro_wiggle.pdf",
    "fig_intro_dilation.pdf", "fig_intro_band.pdf", "fig_intro_two_errors.pdf",
    "fig_intro_averaging.pdf", "fig_intro_atsc.pdf",
    "fig_vsb_standard_model.pdf", "fig_vsb_layout.pdf", "fig_census_map.pdf",
   
    "fig_dirichlet_duality.pdf",
    "fig_model_calibration_layers.pdf", "fig_survey_evidence_flow.pdf",
    "fig_residual_chain_audit.pdf",
    "fig_deployment_lifecycle.pdf",
    "fig_bao_footprint.pdf",
   
}


def main() -> None:
    style.configure(require_tex=True)
    outputs=[]
    for module in (intro_figures,broadcast_figures,detector_figures,framework_figures,forecast_figures):
        outputs.extend(module.build_all())
    names={Path(p).name for p in outputs}
    missing=EXPECTED-names
    extra=names-EXPECTED
    absent={n for n in EXPECTED if not (OUT/n).is_file()}
    if missing or extra or absent:
        raise RuntimeError(f"figure inventory mismatch: missing={sorted(missing|absent)}, extra={sorted(extra)}")
    print(f"Generated {len(outputs)} vector PDFs in {OUT}")

if __name__ == "__main__": main()
