# Disposition of the supplied review

## Review items not applicable to this source version

The alleged missing `xi(r)`, redshift `z`, `sigma`, `theta`, malformed
`2.4 sigma`, channel-36 formatting, duplicate “curve,” and hanging citation
errors were not present in the supplied LaTeX source or its rendered PDF. They
were therefore not introduced as edits. They appear to have come from stale or
faulty text extraction.

The conversational pedagogical voice was retained. Long multi-clause sentences
were split selectively, but memorable headings were not replaced wholesale by
bureaucratic equivalents.

## Review items applied directly

- Displayed `H_0` and `H_1`.
- Defined the noncentrality convention and factor of two.
- Replaced ambiguous register-lane superscripts.
- Specified signed right-shift and rounding behavior.
- Expanded limb-carry and mask-initialization contracts.
- Formalized coherence variables and derivative-stability conditions.
- Added epoch-specific operating-point presentation.
- Added acronym front matter and restructured the abstract.
- Completed Chapters 7, 8, 10, and 11.
- Added a centralized evidence/closing-test appendix.

## Review items corrected rather than copied literally

- Symmetric references do not require a negligible local slope; odd Taylor terms
  cancel under common smooth symmetric sampling. The revision instead identifies
  even curvature and narrow/asymmetric instrumental structure as the limitations.
- A proof that scrambled 8-VSB is exactly Gaussian was not added, because that is
  not true of a complete coded, filtered, synchronized waveform. The text now
  states a narrower noise-like-null argument and requires matched-data ROC tests.
- A universal theorem that pilot detection dominates every cyclostationary method
  was not added. The matched-filter result is confined to its declared signal and
  noise model, and successor methods require matched-compute empirical comparison.
- A full Q15 twiddle table was not moved into the dissertation. The specification,
  generator, hashes, representative values, and golden vectors are the more useful
  reproducibility record.
- Dense transmitter-census and implementation material remains summarized in the
  dissertation; machine-readable products and complete source belong in a versioned
  release rather than as many pages of static appendix output.

## Additional corrections added after independent review

- Corrected the ATSC exact-versus-nominal roll-off/pilot geometry.
- Acknowledged deterministic ATSC synchronization structures.
- Separated the pilot-power proxy from complex visibility residuals.
- Separated stochastic variance from coherent systematic bias.
- Corrected contradictory observing-time scalings.
- Added residual-template and combined-estimator validation gates.
- Distinguished triggered-archive fractions from unconditional occupancy.
- Narrowed optimality, deployment, recovery, and detector-independent claims.
- Reconciled channel counts, epoch status, and archive-versus-live language.
