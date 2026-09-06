#!/usr/bin/env python3
"""Fail closed if the dissertation's vendored result evidence has changed."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from collections.abc import Callable
from pathlib import Path, PurePosixPath
from typing import Any, NamedTuple

FORECAST_DIR = Path("evidence/bao_forecast_completion")
FORECAST_MANIFEST = FORECAST_DIR / "forecast_completion_release_manifest.json"
FORECAST_MANIFEST_SHA = "2410fbbce717b0239bf952c4b32b57e4f586749cc64235d4f9484fbdbf95aa0c"
FORECAST_ARTIFACT_NAMES = (
    "forecast_completion_all_dtv_bins.json",
    "forecast_completion_all_dtv_bins_k_shell_localized.json",
    "forecast_completion_all_dtv_bins_low_kparallel.json",
    "forecast_completion_all_dtv_bins_wedge_like.json",
    "forecast_completion_template_comparison.csv",
    "forecast_completion_channel_mapping.csv",
    "forecast_completion_template_status.csv",
    "forecast_completion_channel_tolerances.png",
    "forecast_completion_channel_tolerances.pdf",
    "forecast_completion_template_summary.tex",
    "forecast_completion_channel_tolerances_caption.txt",
)
FORECAST_SCHEMA_NAME = "forecast-completion-release-manifest.schema.json"
FORECAST_PATH_MAP = {f"out/{name}": name for name in FORECAST_ARTIFACT_NAMES} | {
    f"docs/{FORECAST_SCHEMA_NAME}": FORECAST_SCHEMA_NAME,
}
RECONCILED_FORECAST_DIR = Path(
    "evidence/bao_forecast_completion_20260824_reconciliation"
)
RECONCILED_FORECAST_MANIFEST = (
    RECONCILED_FORECAST_DIR / "forecast_completion_release_manifest.json"
)
RECONCILED_FORECAST_MANIFEST_SHA = (
    "aed22ee6d4d780bdc0ec3a234fecebe7d6f554a3d1593db945f468499de2e381"
)
RECONCILED_FORECAST_PATH_MAP = {
    f"out/forecast_completion_20260824_reconciliation/{name}": name
    for name in FORECAST_ARTIFACT_NAMES
} | {f"docs/{FORECAST_SCHEMA_NAME}": FORECAST_SCHEMA_NAME}


class ForecastRelease(NamedTuple):
    label: str
    directory: Path
    manifest: Path
    manifest_sha: str
    path_map: dict[str, str]
    mirror_pdf: bool


FORECAST_RELEASES = (
    ForecastRelease(
        "forecast",
        FORECAST_DIR,
        FORECAST_MANIFEST,
        FORECAST_MANIFEST_SHA,
        FORECAST_PATH_MAP,
        False,
    ),
    ForecastRelease(
        "reconciled forecast",
        RECONCILED_FORECAST_DIR,
        RECONCILED_FORECAST_MANIFEST,
        RECONCILED_FORECAST_MANIFEST_SHA,
        RECONCILED_FORECAST_PATH_MAP,
        True,
    ),
)

DIGITAL_TRANSFER_PAYLOADS = (
    "README.md",
    "data/analysis.json",
    "data/plot_points.csv",
    "data/qc.json",
    "figures/fig_estimator_transfer_digital.pdf",
    "figures/fig_estimator_transfer_digital.png",
    "raw/raw_input_inventory.csv",
    "run/conditioning.json",
    "run/source_provenance.json",
)
OTA_TRANSFER_PAYLOADS = (
    "README.md",
    "data/analysis.json",
    "data/plot_points.csv",
    "data/qc.json",
    "data/sdr_transfer_summary.csv",
    "data/sdr_transfer_trials.csv",
    "figures/fig_estimator_transfer_ota.pdf",
    "figures/fig_estimator_transfer_ota.png",
    "raw/raw_capture_inventory.csv",
    "run/events.jsonl",
    "run/run_plan.json",
    "run/run_state.json",
    "run/source_provenance.json",
    *(f"run/sessions/pass_{number:02d}.json" for number in range(1, 31)),
)


class TransferRelease(NamedTuple):
    label: str
    directory: Path
    experiment: str
    manifest_sha: str
    checksum_sha: str
    payloads: tuple[str, ...]
    plot_rows: int
    inventory_path: str
    inventory_rows: int
    counts: dict[str, int]
    publication_pdf: str
    mirror_pdf: Path
    other_rows: tuple[tuple[str, int, str], ...]


TRANSFER_RELEASES = (
    TransferRelease(
        "digital estimator transfer",
        Path("evidence/estimator_transfer_20260825"),
        "digital_synthetic",
        "699590c5b814c938b3a47ed6496da74ac7bfb59b558f0db3075d76e29f39d29a",
        "a4e83e3ba5108e31d2978086d4da3cc97e63326bd9f8f4420f659128f59e4603",
        DIGITAL_TRANSFER_PAYLOADS,
        41,
        "raw/raw_input_inventory.csv",
        120,
        {
            "plot_points": 41,
            "raw_source_files": 120,
            "raw_shards": 40,
            "trials": 9000,
        },
        "figures/fig_estimator_transfer_digital.pdf",
        Path("figs/fig_estimator_transfer_digital.pdf"),
        (),
    ),
    TransferRelease(
        "over-the-air estimator transfer",
        Path("evidence/sdr_ota_transfer_20260825"),
        "sdr_ota",
        "a87c172cf3e2d26c610da8cdb3819df39ec1f1a5676da88f1b4df78a29cdc6b1",
        "d611abd964fe28dc3fe754a4722196f642b07f6b955e1c413ca5ef43746b48ab",
        OTA_TRANSFER_PAYLOADS,
        15,
        "raw/raw_capture_inventory.csv",
        1980,
        {
            "events": 1980,
            "mixtures": 1800,
            "passes": 30,
            "plot_points": 15,
            "raw_captures": 1980,
        },
        "figures/fig_estimator_transfer_ota.pdf",
        Path("figs/fig_ota_estimator_transfer.pdf"),
        (
            ("data/sdr_transfer_summary.csv", 15, "csv"),
            ("data/sdr_transfer_trials.csv", 1800, "csv"),
            ("run/events.jsonl", 1980, "jsonl"),
        ),
    ),
)

ARCHIVE_DIR = Path("evidence/canfar_archive_health_v1")
ARCHIVE_COMMIT = "2cf4d8cdc94a2beb2299f2b7ece0dcfe2662c6ee"
ARCHIVE_MANIFEST_SHA = "5bf7809cffc9c77eab44dae9a855996422f347a969a14344d0b2414920ba4e78"
ARCHIVE_DISSERTATION_AUDIT_SHA = (
    "6061cfb872fef49234cbfde0f3a64045aeb3c056d7bb87655f108f1435560133"
)
ARCHIVE_CORE_HASHES = {
    "archive_health_summary.json":
        "7ce08b84ddbdf05cdce5010abc27ec092e062b7656def1599704b58846f62389",
    "archive_exclusion_ledger.jsonl":
        "b3b804273abc8ee55d7dfcc5ce969b89203de435a36a50cbbf539b3fbe42bfd0",
    "health_corrected_integrated_spectra.npz":
        "02b822132a7aa5929f3d60165e0541ff7e775b045e46c4866f58ef7e358e4fa1",
    "diagnostic_manifest.json": ARCHIVE_MANIFEST_SHA,
}
ARCHIVE_DISSERTATION_FIGURES = {
    "fig_bao_time_vs_masking.pdf":
        "2ca7b470eae747df68ee5276defcae353d05f3cefc383e9dc7d1c2c9d59a2e0a",
    "fig_census_psd.pdf":
        "e3f128f5b66c7397f14d1aaa6d046a7c95d2ddee551dc289c248110bce2cd195",
    "fig_census_psd_lower.pdf":
        "408191514b129475fb0ac45cbb8b703cbeae33f36a9ec546279243ee72b4efe4",
}
CURRENT_DISSERTATION_FIGURES = ARCHIVE_DISSERTATION_FIGURES | {
    "fig_bao_time_vs_masking.pdf":
        "8017daee7f8ebd1bcc39b8b5413f18ae4dc1d6411f735b41284a9b759bb3afbc",
}
ARCHIVE_DISSERTATION_DATA = {
    "dissertation_exports/bao_channel_chain_v4.csv":
        "254d57ad289a0417966a397987733507032b65fc6e5f3ca9b6b6b28b898bf99d",
    "dissertation_exports/bao_time_vs_masking.csv":
        "0744902999609124875d7644b6b36719762588c36954716a9e16623e9cccc85a",
    "dissertation_exports/census_psd.csv":
        "0fd2def562f6129838ad031c2d556c55b229e253c249d601c0adb563b9e59b9c",
    "dissertation_exports/worked_example_spectra.csv":
        "0e993bc91c14f483059a84785d6619bfc4ea08fc5d0aa946060ea3313d02c084",
    "dissertation_policy/policy_data.json":
        "df416866df5d1e0f2a07e3a736e10edaf642d637ccf052b3aff92ed2a3d1fe24",
    "dissertation_report/report_data.json":
        "0b1bd4f9340c4aa81e4f3b4243c47a53e3b49fbc930e7dd8d424e0d75278ef9b",
    "dissertation_report/threshold_sweeps.json":
        "f2eaa74a86926a57ea3a56f6f9998f171687a9c0efd2e34b4bc573650417a341",
    "dissertation_status_v4/channel_status_v4.csv":
        "f34bf3cfe9a3d2b28cb5ffa6e117640bffc36113a6fd388f6c35a5edb2262260",
    "dissertation_status_v4/dissertation_summary_v4.json":
        "dd29978368a6c0a7075956c7c7c9c9f7a7770adb0f1a581f86cbf1fd458bf76b",
    "dissertation_status_v4/epoch_operating_points_v4.csv":
        "e6febbd85fb6721b150830b2ef565d38ca98f7326ca2f8111d69e702488d948b",
}
CHANNEL_FREQ = dict(zip(range(14, 37), (
    844, 829, 813, 798, 783, 767, 752, 736, 721, 706, 690, 675,
    660, 644, 629, 614, 598, 583, 568, 552, 537, 521, 506,
)))
FIGURE_FILES = {
    "fine_f_utc_monthly_mean_heatmap": "fine_f_utc_monthly_heatmap.png",
    "health_filtered_scalar_histograms": "health_filtered_histograms.pdf",
    "per_channel_dissertation_diagnostic_atlas":
        "channel_{channel}_diagnostic_atlas.pdf",
    "relative_time_averaged_health_corrected_spectra": "relative_time_averaged_spectra.pdf",
}

AUDIT_VALUES = {
    "schema_version": "dissertation_canfar_archive_audit_v3",
    "inputs/per_pilot_archive/sha256":
        "c78f4fa8a3b9c11bd22344360ea224c3f88ee8e39276fd61ed15f4e989210aaa",
    "inputs/per_pilot_archive/size_bytes": 728281286,
    "inputs/inventory_archive/sha256":
        "bc975ac7c97a70f2871eaec166136f5944c98ade1b658cdfdc6a7fa1ee5c697f",
    "inputs/inventory_archive/size_bytes": 2251998,
    "inputs/detector_kernel/sha256":
        "c85f50ddf898517bc0101d1882c854c3df70b09f0ab0b58803dc32f59e3c6d12",
    "inputs/detector_kernel/version": "2.1.0",
    "inputs/detector_kernel/profile_length": 128,
    "inputs/detector_kernel/profiles": 3,
    "inputs/detector_kernel/component_bits": 4,
    "survey_enumeration/enumerated_events": 16327,
    "survey_enumeration/outrigger_labelled_excluded_events": 6140,
    "survey_enumeration/survey_target_events": 10187,
    "survey_enumeration/completed_events": 10184,
    "survey_enumeration/pending_attempt_category_events": 3,
    "survey_enumeration/retried_scope_events": 3,
    "survey_enumeration/retry_attempt_count_distribution/2": 3,
    "survey_enumeration/completed_with_inventory_rows": 9214,
    "survey_enumeration/completed_aged_out_empty": 107,
    "survey_enumeration/completed_without_common_target_path_derived": 863,
    "survey_enumeration/inventory_rows": 170377,
    "survey_enumeration/inventory_unique_rows": 170377,
    "survey_enumeration/inventory_duplicate_rows": 0,
    "survey_enumeration/catalogued_object_bytes": 28237618443352,
    "product_inventory/physical_channels": list(range(14, 37)),
    "product_inventory/npz_products": 23,
    "product_inventory/event_channel_units": 170374,
    "product_inventory/zero_frame_event_channel_units": 4692,
    "product_inventory/distinct_source_events": 9214,
    "product_inventory/distinct_source_events_with_archived_valid_frames": 8983,
    "product_inventory/distinct_source_events_with_health_included_frames": 8980,
    "product_inventory/stored_frames": 750461,
    "product_inventory/archived_denominator_valid_frames": 750457,
    "product_inventory/explicit_invalid_frames": 4,
    "product_inventory/health_included_frames": 750279,
    "product_inventory/quarantined_raw_objects": 3,
    "health_filtered_exposure/frames_with_reproducible_timestamp_and_duration": 747790,
    "health_filtered_exposure/triggered/processed_event_channel_units": 166581,
    "health_filtered_exposure/triggered/health_included_frames": 699579,
    "health_filtered_exposure/triggered/frames_with_reproducible_duration": 697090,
    "health_filtered_exposure/triggered/health_included_exposure_seconds": 29238.0737536,
    "health_filtered_exposure/scheduled/processed_event_channel_units": 3793,
    "health_filtered_exposure/scheduled/health_included_frames": 50700,
    "health_filtered_exposure/scheduled/frames_with_reproducible_duration": 50700,
    "health_filtered_exposure/scheduled/health_included_exposure_seconds": 2126.512128,
    "health_gate/gate_id": "pilotproxy_archive_frame_health_gate_v1",
    "health_gate/excluded_unique_frames": 182,
    "health_gate/health_included_frames": 750279,
    "health_gate/reason_counts/detector_invalid": 4,
    "health_gate/reason_counts/detector_powers_all_zero": 4,
    "health_gate/reason_counts/native_complex_int4_mean_power_ceiling": 178,
    "ceiling_power_population/frames": 178,
    "ceiling_power_population/distinct_source_events": 8,
    "ceiling_power_population/event_channel_units": 70,
    "ceiling_power_population/event_channel_units_containing_only_ceiling_frames": 50,
    "aggregate_spectrum_repair/power_per_frame_at_unshifted_bin_0": 70368739983360,
    "aggregate_spectrum_repair/frames_subtracted_from_before_mask": 178,
    "aggregate_spectrum_repair/frames_subtracted_from_after_mask": 118,
    "aggregate_spectrum_repair/ceiling_frames_already_rejected": 60,
    "aggregate_spectrum_repair/parseval_relative_tolerance": 5e-7,
    "immutable_release/producer_repository": "WVURAIL/pilot-proxy",
    "immutable_release/producer_commit": ARCHIVE_COMMIT,
    "immutable_release/producer_worktree_clean": True,
    "immutable_release/diagnostic_asset_count": 92,
    "provenance_availability/retry_counts_and_attempt_multiplicity": True,
}


class Verify:
    def __init__(self, root: Path) -> None:
        self.root, self.errors, self.checks = root, [], 0

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def equal(self, actual: Any, expected: Any, label: str) -> None:
        self.checks += 1
        if actual != expected:
            self.fail(f"{label}: expected {expected!r}, found {actual!r}")

    def true(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.fail(message)

    def json(self, relative: Path, label: str) -> Any:
        def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate object key {key!r}")
                result[key] = value
            return result

        try:
            return json.loads(
                (self.root / relative).read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_keys,
            )
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            self.fail(f"{label}: cannot read {relative.as_posix()}: {exc}")
            return None

    def sha(self, relative: Path, expected: str, size: int | None = None) -> None:
        self.checks += 1
        try:
            data = (self.root / relative).read_bytes()
        except OSError as exc:
            self.fail(f"{relative.as_posix()}: cannot read artifact: {exc}")
            return
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            self.fail(
                f"{relative.as_posix()}: SHA-256 expected {expected}, "
                f"found {actual}"
            )
        if size is not None:
            self.equal(len(data), size, f"{relative.as_posix()} size")

    def same_file(self, left: Path, right: Path, label: str) -> None:
        self.checks += 1
        try:
            with (
                (self.root / left).open("rb") as left_file,
                (self.root / right).open("rb") as right_file,
            ):
                while True:
                    left_block = left_file.read(1024 * 1024)
                    right_block = right_file.read(1024 * 1024)
                    if left_block != right_block:
                        self.fail(f"{label}: files differ")
                        return
                    if not left_block:
                        return
        except OSError as exc:
            self.fail(f"{label}: cannot compare files: {exc}")

    def relation(self, label: str, function: Callable[[], tuple[Any, Any]]) -> None:
        try:
            actual, expected = function()
        except (KeyError, TypeError, ValueError) as exc:
            self.fail(f"{label}: cannot evaluate invariant: {exc}")
            return
        self.equal(actual, expected, label)


def at(document: Any, slash_path: str) -> Any:
    value = document
    for component in slash_path.split("/"):
        if not isinstance(value, dict) or component not in value:
            raise KeyError(slash_path)
        value = value[component]
    return value


def safe_path(value: Any) -> bool:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or any(ord(character) < 32 for character in value)
    ):
        return False
    try:
        path = PurePosixPath(value)
    except (TypeError, ValueError):
        return False
    return (
        path.as_posix() == value
        and not path.is_absolute()
        and not ({"", ".", ".."} & set(path.parts))
    )


def csv_row_count(v: Verify, relative: Path, label: str) -> int | None:
    try:
        with (v.root / relative).open(newline="", encoding="utf-8") as stream:
            reader = csv.reader(stream)
            header = next(reader)
            v.true(
                bool(header) and all(header) and len(header) == len(set(header)),
                f"{label}: invalid header",
            )
            count = 0
            for line_number, row in enumerate(reader, 2):
                count += 1
                if len(row) != len(header):
                    v.fail(
                        f"{label}: line {line_number} has {len(row)} fields; "
                        f"expected {len(header)}"
                    )
            return count
    except (OSError, UnicodeError, csv.Error, StopIteration) as exc:
        v.fail(f"{label}: cannot read {relative.as_posix()}: {exc}")
        return None


def jsonl_row_count(v: Verify, relative: Path, label: str) -> int | None:
    try:
        count = 0
        with (v.root / relative).open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    raise ValueError(f"blank line {line_number}")
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise TypeError(f"line {line_number} is not an object")
                count += 1
        return count
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        v.fail(f"{label}: cannot read {relative.as_posix()}: {exc}")
        return None


def checksum_rows(v: Verify, relative: Path, label: str) -> dict[str, str] | None:
    try:
        lines = (v.root / relative).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        v.fail(f"{label}: cannot read {relative.as_posix()}: {exc}")
        return None
    rows: dict[str, str] = {}
    for line_number, line in enumerate(lines, 1):
        if len(line) < 67 or line[64:66] != "  ":
            v.fail(f"{label}: malformed line {line_number}")
            continue
        digest, path = line[:64], line[66:]
        if any(character not in "0123456789abcdef" for character in digest):
            v.fail(f"{label}: invalid digest on line {line_number}")
            continue
        if not safe_path(path):
            v.fail(f"{label}: unsafe path on line {line_number}: {path!r}")
            continue
        if path in rows:
            v.fail(f"{label}: duplicate path on line {line_number}: {path!r}")
            continue
        rows[path] = digest
    return rows


def verify_transfer_release(v: Verify, release: TransferRelease) -> None:
    manifest_path = release.directory / "release_manifest.json"
    v.sha(manifest_path, release.manifest_sha)
    v.sha(release.directory / "SHA256SUMS", release.checksum_sha)
    manifest = v.json(manifest_path, f"{release.label} release manifest")
    if not isinstance(manifest, dict):
        return
    v.equal(
        manifest.get("schema_version"),
        "estimator_transfer_release_v1",
        f"{release.label} schema",
    )
    v.equal(
        manifest.get("experiment"),
        release.experiment,
        f"{release.label} experiment",
    )
    v.equal(
        manifest.get("path_semantics"),
        "release_root_relative_posix",
        f"{release.label} path semantics",
    )
    v.equal(
        manifest.get("counts"),
        release.counts,
        f"{release.label} counts",
    )
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        v.fail(f"{release.label} manifest artifacts: expected a list")
        return
    v.equal(
        manifest.get("artifact_count"),
        len(release.payloads),
        f"{release.label} artifact count",
    )
    artifact_hashes: dict[str, str] = {}
    publication_digest = None
    publication_size = None
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            v.fail(f"{release.label} artifact {index}: expected an object")
            continue
        path = artifact.get("path")
        digest = artifact.get("sha256")
        size = artifact.get("size_bytes")
        v.true(
            safe_path(path),
            f"{release.label} artifact {index}: unsafe path {path!r}",
        )
        if not isinstance(path, str):
            continue
        if path in artifact_hashes:
            v.fail(f"{release.label} artifact {index}: duplicate path {path!r}")
            continue
        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
            or not isinstance(size, int)
            or size < 0
        ):
            v.fail(f"{release.label} artifact {path}: invalid digest or size")
            continue
        artifact_hashes[path] = digest
        v.sha(release.directory / path, digest, size)
        if path == release.publication_pdf:
            publication_digest = digest
            publication_size = size
    v.equal(
        set(artifact_hashes),
        set(release.payloads),
        f"{release.label} payload census",
    )
    actual_files = {
        path.relative_to(v.root / release.directory).as_posix()
        for path in (v.root / release.directory).rglob("*")
        if path.is_file()
    }
    v.equal(
        actual_files,
        {*release.payloads, "release_manifest.json", "SHA256SUMS"},
        f"{release.label} complete file census",
    )
    sums = checksum_rows(
        v,
        release.directory / "SHA256SUMS",
        f"{release.label} checksum ledger",
    )
    if sums is not None:
        v.equal(
            sums,
            artifact_hashes | {"release_manifest.json": release.manifest_sha},
            f"{release.label} checksum ledger contents",
        )
    v.equal(
        csv_row_count(
            v,
            release.directory / "data/plot_points.csv",
            f"{release.label} plot points",
        ),
        release.plot_rows,
        f"{release.label} plot-point row count",
    )
    v.equal(
        csv_row_count(
            v,
            release.directory / release.inventory_path,
            f"{release.label} raw inventory",
        ),
        release.inventory_rows,
        f"{release.label} raw-inventory row count",
    )
    provenance = v.json(
        release.directory / "run/source_provenance.json",
        f"{release.label} source provenance",
    )
    if isinstance(provenance, dict):
        v.equal(
            provenance.get("schema_version"),
            "estimator_transfer_source_provenance_v1",
            f"{release.label} provenance schema",
        )
        v.equal(
            provenance.get("experiment"),
            release.experiment,
            f"{release.label} provenance experiment",
        )
        try:
            run_worktree = at(provenance, "run_worktree")
            v.equal(
                at(provenance, "run_worktree/base_revision"),
                "e2f9f7fa0d2013822274b2f34a3420d26ca8225b",
                f"{release.label} run base revision",
            )
            v.equal(
                at(provenance, "publication_export/state"),
                "post-run archival regeneration from frozen raw results",
                f"{release.label} publication-export state",
            )
            v.true(
                isinstance(run_worktree, dict)
                and "repository_revision_after_update" not in run_worktree,
                f"{release.label} run provenance is conflated with the later export",
            )
        except (KeyError, TypeError) as exc:
            v.fail(f"{release.label} provenance invariant cannot be evaluated: {exc}")
    for path, expected, kind in release.other_rows:
        relative = release.directory / path
        if kind == "csv":
            actual = csv_row_count(v, relative, f"{release.label} {path}")
        else:
            actual = jsonl_row_count(v, relative, f"{release.label} {path}")
        v.equal(actual, expected, f"{release.label} {path} row count")
    if isinstance(publication_digest, str) and isinstance(publication_size, int):
        v.sha(release.mirror_pdf, publication_digest, publication_size)
        v.same_file(
            release.directory / release.publication_pdf,
            release.mirror_pdf,
            f"{release.label} publication PDF equality",
        )
    else:
        v.fail(f"{release.label} publication PDF is absent from the manifest")


def verify_transfer_releases(v: Verify) -> None:
    for release in TRANSFER_RELEASES:
        verify_transfer_release(v, release)


def verify_forecast_release(v: Verify, release: ForecastRelease) -> None:
    v.sha(release.manifest, release.manifest_sha)
    manifest = v.json(release.manifest, f"{release.label} release manifest")
    if not isinstance(manifest, dict):
        return
    v.equal(manifest.get("schema"),
            "baonoise-forecast-completion-release-manifest-v2",
            f"{release.label} schema")
    v.equal(manifest.get("schema_version"), 2,
            f"{release.label} schema version")
    v.equal(manifest.get("artifact_count"), 12,
            f"{release.label} artifact count")
    v.equal(manifest.get("absolute_paths_included"), False,
            f"{release.label} absolute-path flag")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        v.fail(f"{release.label} manifest artifacts: expected a list")
        return
    seen, schema_sha = set(), None
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            v.fail(f"{release.label} artifact {index}: expected an object")
            continue
        source = artifact.get("path")
        v.true(
            safe_path(source),
            f"{release.label} artifact {index}: unsafe producer path {source!r}",
        )
        if not isinstance(source, str):
            continue
        seen.add(source)
        target = release.path_map.get(source)
        if target is None:
            v.fail(
                f"{release.label} artifact {index}: "
                f"unapproved producer path {source!r}"
            )
            continue
        digest, size = artifact.get("sha256"), artifact.get("size_bytes")
        if not isinstance(digest, str) or len(digest) != 64 or not isinstance(size, int):
            v.fail(f"{release.label} artifact {source}: invalid digest or size")
            continue
        v.sha(release.directory / target, digest, size)
        if release.mirror_pdf and target == "forecast_completion_channel_tolerances.pdf":
            v.sha(Path("figs/fig_bao_template_tolerances.pdf"), digest, size)
        if source.startswith("docs/"):
            schema_sha = digest
    v.equal(
        seen,
        set(release.path_map),
        f"{release.label} producer-path/basename mapping",
    )
    v.equal(
        manifest.get("manifest_schema_sha256"),
        schema_sha,
        f"{release.label} schema digest",
    )


def verify_forecast_releases(v: Verify) -> None:
    for release in FORECAST_RELEASES:
        verify_forecast_release(v, release)


def figure_path(channel: int, freq: int, kind: str) -> str:
    filename = FIGURE_FILES[kind].format(channel=channel)
    return f"figures/channel_{channel}_fid_{freq:04d}/{filename}"


def verify_archive_manifest(v: Verify) -> None:
    for name, digest in ARCHIVE_CORE_HASHES.items():
        v.sha(ARCHIVE_DIR / name, digest)
    for name, digest in ARCHIVE_DISSERTATION_DATA.items():
        v.sha(ARCHIVE_DIR / name, digest)
    data_directories = {
        "dissertation_exports",
        "dissertation_policy",
        "dissertation_report",
        "dissertation_status_v4",
    }
    actual_data_paths = {
        path.relative_to(v.root / ARCHIVE_DIR).as_posix()
        for directory in data_directories
        for path in (v.root / ARCHIVE_DIR / directory).rglob("*")
        if path.is_file()
    }
    v.equal(
        actual_data_paths,
        set(ARCHIVE_DISSERTATION_DATA),
        "CANFAR dissertation-data path census",
    )
    for name, digest in ARCHIVE_DISSERTATION_FIGURES.items():
        v.sha(ARCHIVE_DIR / "dissertation_figures_v4" / name, digest)
        v.sha(Path("figs") / name, CURRENT_DISSERTATION_FIGURES[name])
    manifest = v.json(ARCHIVE_DIR / "diagnostic_manifest.json", "CANFAR diagnostic manifest")
    if not isinstance(manifest, dict):
        return
    fixed = {
        "schema_version": "pilotproxy_archive_diagnostic_manifest_v1",
        "path_semantics": "release_root_relative_posix",
        "summary": "archive_health_summary.json",
        "exclusion_ledger": "archive_exclusion_ledger.jsonl",
        "corrected_spectra": "health_corrected_integrated_spectra.npz",
    }
    for key, expected in fixed.items():
        v.equal(manifest.get(key), expected, f"CANFAR manifest {key}")
    generator = manifest.get("generator", {})
    v.equal(generator.get("git_commit") if isinstance(generator, dict) else None,
            ARCHIVE_COMMIT, "CANFAR manifest producer commit")
    v.equal(generator.get("git_tracked_worktree_clean") if isinstance(generator, dict) else None,
            True, "CANFAR manifest clean-worktree flag")
    figures = manifest.get("figures")
    if not isinstance(figures, list):
        v.fail("CANFAR manifest figures: expected a list")
        return
    expected_paths = {
        figure_path(channel, freq, kind)
        for channel, freq in CHANNEL_FREQ.items()
        for kind in FIGURE_FILES
    }
    seen, channel_kinds = set(), defaultdict(Counter)
    for index, figure in enumerate(figures):
        if not isinstance(figure, dict):
            v.fail(f"CANFAR figure {index}: expected an object")
            continue
        path, channel, freq, kind = (figure.get(key) for key in
                                     ("path", "physical_channel", "freq_id", "kind"))
        v.true(safe_path(path), f"CANFAR figure {index}: unsafe path {path!r}")
        if isinstance(path, str) and path in seen:
            v.fail(f"CANFAR figure {index}: duplicate path {path!r}")
        if (not isinstance(path, str) or not isinstance(channel, int)
                or channel not in CHANNEL_FREQ or not isinstance(kind, str)
                or kind not in FIGURE_FILES):
            v.fail(f"CANFAR figure {index}: invalid path/channel/kind")
            continue
        seen.add(path)
        channel_kinds[channel][kind] += 1
        v.equal(freq, CHANNEL_FREQ[channel], f"CANFAR figure {index} freq_id")
        v.equal(path, figure_path(channel, freq, kind), f"CANFAR figure {index} path")
        v.equal(figure.get("relative_path"), path, f"CANFAR figure {index} relative_path")
        digest = figure.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            v.fail(f"CANFAR figure {index}: invalid sha256")
        else:
            v.sha(ARCHIVE_DIR / path, digest)
            if kind == "per_channel_dissertation_diagnostic_atlas":
                v.sha(
                    Path("figs/archive_health_v1")
                    / f"channel_{channel}_diagnostic_atlas.pdf",
                    digest,
                )
    v.equal(len(figures), 92, "CANFAR diagnostic figure count")
    v.equal(seen, expected_paths, "CANFAR diagnostic figure path set")
    one_each = Counter({kind: 1 for kind in FIGURE_FILES})
    for channel in CHANNEL_FREQ:
        v.equal(channel_kinds[channel], one_each, f"CANFAR channel {channel} figure census")


def verify_audit(v: Verify) -> None:
    v.sha(Path("CANFAR_PRODUCT_HEALTH_AUDIT.json"), ARCHIVE_DISSERTATION_AUDIT_SHA)
    audit = v.json(Path("CANFAR_PRODUCT_HEALTH_AUDIT.json"), "CANFAR dissertation audit")
    if not isinstance(audit, dict):
        return
    for path, expected in AUDIT_VALUES.items():
        try:
            actual = at(audit, path)
        except KeyError:
            v.fail(f"CANFAR audit invariant {path}: missing")
            continue
        v.equal(actual, expected, f"CANFAR audit invariant {path}")
    digest_fields = {
        "archive_health_summary.json": "archive_health_summary_sha256",
        "archive_exclusion_ledger.jsonl": "archive_exclusion_ledger_sha256",
        "health_corrected_integrated_spectra.npz": "health_corrected_integrated_spectra_sha256",
        "diagnostic_manifest.json": "diagnostic_manifest_sha256",
    }
    for name, field in digest_fields.items():
        v.relation(f"CANFAR audit immutable {field}",
                   lambda n=name, f=field: (at(audit, f"immutable_release/{f}"),
                                             ARCHIVE_CORE_HASHES[n]))

    relations = {
        "survey target partition": lambda: (
            at(audit, "survey_enumeration/enumerated_events")
            - at(audit, "survey_enumeration/outrigger_labelled_excluded_events"),
            at(audit, "survey_enumeration/survey_target_events")),
        "survey completion partition": lambda: (
            at(audit, "survey_enumeration/completed_events")
            + at(audit, "survey_enumeration/pending_attempt_category_events"),
            at(audit, "survey_enumeration/survey_target_events")),
        "completed-event disposition partition": lambda: (
            at(audit, "survey_enumeration/completed_with_inventory_rows")
            + at(audit, "survey_enumeration/completed_aged_out_empty")
            + at(audit, "survey_enumeration/completed_without_common_target_path_derived"),
            at(audit, "survey_enumeration/completed_events")),
        "inventory uniqueness partition": lambda: (
            at(audit, "survey_enumeration/inventory_unique_rows")
            + at(audit, "survey_enumeration/inventory_duplicate_rows"),
            at(audit, "survey_enumeration/inventory_rows")),
        "product/quarantine reconciliation": lambda: (
            at(audit, "product_inventory/event_channel_units")
            + at(audit, "product_inventory/quarantined_raw_objects"),
            at(audit, "survey_enumeration/inventory_rows")),
        "health-frame reconciliation": lambda: (
            at(audit, "product_inventory/stored_frames")
            - at(audit, "health_gate/excluded_unique_frames"),
            at(audit, "product_inventory/health_included_frames")),
        "archived-valid denominator": lambda: (
            at(audit, "product_inventory/stored_frames")
            - at(audit, "product_inventory/explicit_invalid_frames"),
            at(audit, "product_inventory/archived_denominator_valid_frames")),
        "observation-class frame partition": lambda: (
            at(audit, "health_filtered_exposure/triggered/health_included_frames")
            + at(audit, "health_filtered_exposure/scheduled/health_included_frames"),
            at(audit, "product_inventory/health_included_frames")),
        "timed-exposure frame partition": lambda: (
            at(audit, "health_filtered_exposure/triggered/frames_with_reproducible_duration")
            + at(audit, "health_filtered_exposure/scheduled/frames_with_reproducible_duration"),
            at(audit,
               "health_filtered_exposure/frames_with_reproducible_timestamp_and_duration")),
        "untimed health-frame count": lambda: (
            at(audit, "product_inventory/health_included_frames")
            - at(audit,
                 "health_filtered_exposure/frames_with_reproducible_timestamp_and_duration"),
            2489),
        "before-mask spectrum repair": lambda: (
            at(audit, "aggregate_spectrum_repair/frames_subtracted_from_before_mask"),
            at(audit, "ceiling_power_population/frames")),
        "after-mask spectrum repair partition": lambda: (
            at(audit, "aggregate_spectrum_repair/frames_subtracted_from_after_mask")
            + at(audit, "aggregate_spectrum_repair/ceiling_frames_already_rejected"),
            at(audit, "ceiling_power_population/frames")),
    }
    for label, relation in relations.items():
        v.relation(f"CANFAR audit {label}", relation)
    try:
        discrepancy = at(audit, "aggregate_spectrum_repair/worst_parseval_relative_discrepancy")
        tolerance = at(audit, "aggregate_spectrum_repair/parseval_relative_tolerance")
        v.true(isinstance(discrepancy, (int, float)) and 0 <= discrepancy <= tolerance,
               f"CANFAR audit Parseval discrepancy {discrepancy!r} exceeds {tolerance!r}")
    except (KeyError, TypeError) as exc:
        v.fail(f"CANFAR audit Parseval invariant cannot be evaluated: {exc}")

    ledger_path = ARCHIVE_DIR / "archive_exclusion_ledger.jsonl"
    rows = []
    try:
        for number, line in enumerate((v.root / ledger_path).read_text().splitlines(), 1):
            row = json.loads(line)
            if not isinstance(row, dict):
                raise TypeError(f"line {number} is not an object")
            rows.append(row)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        v.fail(f"{ledger_path.as_posix()}: cannot parse ledger: {exc}")
        return
    keys = [row.get("ledger_key") for row in rows]
    reasons: Counter[str] = Counter()
    for number, row in enumerate(rows, 1):
        reason_codes = row.get("reason_codes")
        if not isinstance(reason_codes, list) or not all(
                isinstance(reason, str) for reason in reason_codes):
            v.fail(f"CANFAR exclusion-ledger line {number}: invalid reason_codes")
            continue
        reasons.update(reason_codes)
    expected_reasons = Counter({
        "baseband_power_at_negative_full_scale_ceiling": 178,
        "detector_invalid": 4,
        "detector_powers_all_zero": 4,
    })
    v.equal(len(rows), 182, "CANFAR exclusion-ledger row count")
    v.true(all(isinstance(key, str) and key for key in keys),
           "CANFAR exclusion ledger contains an invalid ledger_key")
    if all(isinstance(key, str) for key in keys):
        v.equal(len(set(keys)), len(keys), "CANFAR exclusion-ledger key uniqueness")
    v.equal(reasons, expected_reasons, "CANFAR exclusion-ledger reason census")

    summary = v.json(ARCHIVE_DIR / "archive_health_summary.json", "CANFAR archive summary")
    if isinstance(summary, dict):
        for path, expected in {
            "schema_version": "pilotproxy_archive_health_summary_v1",
            "totals/products": 23,
            "totals/stored_frames": 750461,
            "totals/included_frames": 750279,
            "totals/excluded_unique_frames": 182,
            "totals/reason_counts": dict(expected_reasons),
            "provenance/audit_implementation/git_commit": ARCHIVE_COMMIT,
            "provenance/audit_implementation/git_tracked_worktree_clean": True,
        }.items():
            try:
                actual = at(summary, path)
            except KeyError:
                v.fail(f"CANFAR archive summary invariant {path}: missing")
            else:
                v.equal(actual, expected, f"CANFAR archive summary invariant {path}")


def main() -> int:
    verifier = Verify(Path(__file__).resolve().parents[1])
    verify_transfer_releases(verifier)
    verify_forecast_releases(verifier)
    verify_archive_manifest(verifier)
    verify_audit(verifier)
    if verifier.errors:
        print(f"Vendored evidence verification FAILED ({len(verifier.errors)} errors):",
              file=sys.stderr)
        for error in verifier.errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(
        "Vendored evidence verification passed: "
        f"{verifier.checks} checks; "
        f"{sum(len(release.payloads) for release in TRANSFER_RELEASES)} "
        "estimator-transfer payloads in two releases, "
        "24 forecast artifacts in two releases, "
        "4 CANFAR core files, "
        "10 dissertation data products, 3 archive result PDFs, 92 diagnostic "
        f"figures, {27 + len(TRANSFER_RELEASES)} active figure copies, "
        "and 182 ledger rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
