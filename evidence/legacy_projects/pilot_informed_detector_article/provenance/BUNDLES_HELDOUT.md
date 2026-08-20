# Large provenance artifacts held out of the manuscript zip (size cap)

Both canonical results bundles are part of the paper's provenance but
are excluded from the manuscript zip to stay under delivery limits.
Both originate from Dylan's CANFAR runs and are in his possession; they
are also archived in the paper workspace. Integrity:

be7e3d5767bf96d8a24d1e0409a860728235d7ed2dd5ebe0ae3399a01f396496  results_bundle_chime-pilots_20260717T040435Z.tar.gz
16fba766541e165661f86810dac1e5efb5d9e57afdeaddadb1becb835b0c571b  results_bundle_chime-pilots_20260717T162658Z_stack1829.tar.gz

- 040435Z = production results (recorded 1548 stack, max-events mode)
- 162658Z = stack-robustness run (unrestricted 1829 block, explicit mode)

Also held out: run_pd_curves_cpu_1000.tar.gz (11 MB; the archived
45k-trial CPU sweep records, in Dylan's possession and the paper
workspace).

Added for review round 10 per R9's request: all_spectra.npz (5.3 MB,
the raw full-depth integrated-spectra arrays behind the tone inventory
and supplementary spectra) plus survey_composition_by_channel.csv,
survey_quarterly_exposure.csv, survey_frb_stratum_rates.csv, and
instrument_tones.csv.
