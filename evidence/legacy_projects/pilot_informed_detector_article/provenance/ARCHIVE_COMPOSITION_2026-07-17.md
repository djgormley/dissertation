# Archive inventory composition — measured 2026-07-17

Source: chimepilots.zip (datatrawl inventory for chime-pilots, created
2026-07-03T22:06:59Z; scopes chime.event.baseband.raw +
chime.scheduled.baseband.raw). inventory.jsonl = 161,872 rows (matches
§6.1 exactly); 8,759 distinct events (8,604 appear in products; the
difference sits in the incomplete/no-files survey lists).

Scope: 158,995 triggered (98.2%) / 2,877 scheduled (1.8%).
Classes: classified.FRB 42.4%; B0531+21 (Crab) commissioning 19.9%;
SGR 8.1%; backlog.pulsar 6.7%; B0329+54 commissioning 6.2%;
classified.PULSAR 5.0%; scheduled.commissioning 1.8%; ODWG.pulsar 1.8%;
missing_l4_actions 1.4%.

Per-channel archive totals vs processed (full-depth = ch24, ch30-36):
ch14 2000/8336, ch15 2000/7959, ch16 2000/8592, ch17 2000/7233,
ch18 2000/8441, ch19 2000/5209, ch20 2000/8485, ch21 2000/8546,
ch22 2000/8275, ch23 2000/8157, ch24 1722/1722 FULL, ch25 2000/8309,
ch26 2000/5342, ch27 2000/6824, ch28 2000/7570, ch29 3200/8371,
ch30 1484/1484 FULL, ch31 6927/6927 FULL, ch32 5118/5118 FULL,
ch33 6511/6511 FULL, ch34 8383/8383 FULL, ch35 8304/8304 FULL,
ch36 7774/7774 FULL.

Archive events by year: 2018: 588, 2019: 12,751, 2020: 14,266,
2021: 15,783, 2022: 11,493, 2023: 21,434, 2024: 25,700, 2025: 40,354,
2026: 19,503.

NSF award title confirmed from the award-search PDF: Grant No. 2307581,
"New Interference Detection, Mitigation, and Fusion Methodologies for
Radio Astronomy" (Standard Grant) — now in the Acknowledgements.

Pending for the full R7 survey-bias item: event_presence_keys dump
(join processed events -> classes for capped channels; quarterly
exposure columns; classified-FRB stratum recompute of secular rates).
inventory.meta.json archived alongside; inventory.jsonl (47 MB) retained
in the session workspace, sha256 recorded on request.
