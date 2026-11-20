# Changelog

All notable changes to `spt_qa_database` are recorded here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Each release is a git tag, and each section names the
alembic revision (`alembic/qadb`) that brings a database to it.

## [Unreleased]

Revision `c9e4f2a6d813`. Goes with drp_qa from 0.5.0.

### Added

- **`qa_normal_value`** (PIPE2D-2013) — each camera's normal value of a metric, for one frame type and lamp or
  species, with the visit it is valid from and who accepted it. The gate's percentage checks compare with it.
- **`detector_health_qa`** (PIPE2D-2013) — the reduction's detector statistics in long format: per amplifier on the
  CCDs, per detector on the n arm (`amplifier` empty).
- **`qa_gate.frame_type`** (PIPE2D-2013) — the frame type judged. Null on rows written before this revision.
- **`image_quality_qa.n_saturated_lines`, `pct_saturated_pixels`** (PIPE2D-2013).
- **`seq_type` on `image_quality_qa` and `dm_line_residual_qa`, `image_quality_qa.lamps`** (PIPE2D-2015) — the raw
  sequence type and the lamps lit, for the frame classification.
- **README: Migrations** — how to apply a migration.

### Changed

- **The numbers the gate reads are double precision** (PIPE2D-2013) — `med_fwhm`, `med_dx_center` and
  `lines_per_fiber` of `image_quality_qa`, `value` of `dm_line_residual_qa_metric`, and `twilight_level_offset`,
  `twilight_resid_rms` and `twilight_patch` of `twilight_qa`. A value already stored keeps its single-precision
  digits.
- **The version comes from the git tag** — `lsst-versions` reads it at build time, as in `drp_qa` and
  `pfs_utils`; `pyproject.toml` no longer states one. A tagged commit builds as its tag and a later one as a development
  version of the next; a clone without the tags builds as a `0.0` development version.
- **Python 3.12 or later** — was 3.10.

### Removed

- **The thresholds tables** (PIPE2D-2013) — `qa_thresholds`, `qa_threshold_entry` and `qa_processing_thresholds`,
  with their rows.
- **Verdict columns of the numbers tables** (PIPE2D-2013) — `qa_status`, `qa_decided_by` and `qa_reason` of
  `image_quality_qa`, `dm_line_residual_qa` and `twilight_qa`; `status` of `dm_line_residual_qa_metric`;
  `recommended_action` of `dm_line_residual_qa`. The verdict is the row of `qa_gate`.
- **`qa_gate.decided_by_task` and `provisional`** (PIPE2D-2013).

What these held is not copied, and the downgrade brings the columns and tables back empty: take a dump before
upgrading. The downgrade also drops what the new tables and columns hold.

### Fixed

- **Column comments** (PIPE2D-2013) — `image_quality_qa.obs_type` and `calexp_run`,
  `dm_line_residual_qa_metric.metric`, and `qa_gate.qa_decided_by` and `qa_reason` say what drp_qa 0.5.0 stores.

## [0.5.0] - 2026-11-10

Revision `acbd1a9681d6`. Goes with drp_qa 0.2.0 to 0.4.1.

### Added

- **`qa_processing_thresholds`** (PIPE2D-1991) — every thresholds layer a task judged a processing's images with,
  in the order judged.

### Removed

- **`qa_gate.iq_thresholds_id`, `dm_thresholds_id`, `twilight_thresholds_id`** (PIPE2D-1991) — what they cited
  became layer 0 of the new table.

## [0.4.0] - 2026-11-10

No revision.

### Changed

- **Packaging in `pyproject.toml`, on psycopg 3** — connect with a `postgresql+psycopg://` URL.
- **Schema diagram** — `diagrams/schema.pdf` is redrawn by a GitHub Action when `models.py` changes on `main`.

## [0.3.0] - 2026-11-05

Revision `5d2e8f71c0b3`. Not tagged.

### Added

- **`twilight_qa`** (INSTRM-3089) — the twilight sequence check per detector image, and
  `qa_gate.twilight_thresholds_id`.

## [0.2.0] - 2026-10-27

Revision `a7c3e5d91b24`.

### Added

- **The per-image gate tables** (PIPE2D-1385) — `image_quality_qa`, `image_quality_qa_species`,
  `dm_line_residual_qa`, `dm_line_residual_qa_metric`, `qa_thresholds`, `qa_threshold_entry` and `qa_gate`.
- **`data_processing_pipe2d.datamodel_version`, `obs_pfs_version`** (PIPE2D-1385).

### Removed

- **`detector_map_qa`** (PIPE2D-1385) — never written.

## [0.1.1] - 2026-07-07

Revision `348db3f79d46`.

### Changed

- **`data_processing_pipe2d` is unique on collection and RUN** (PIPE2D-1860).
- **`flux_cal_qa.merged_filter` and `merged_color_filters` are text.**

## [0.1.0] - 2026-06-25

Revision `f6f47983358a`.

### Added

- **Tables for the DRP's QA** (PIPE2D-1385) — `data_processing_pipe2d`, `detector_map_qa`, `extraction_qa`,
  `flux_cal_qa` and the `sky_subtraction_qa_sa` tables.
- **`data_qa.pipe2d_version`, `drp_qa_version`, `process_type`** (PIPE2D-1385).

### Removed

- **`data_processing`, `data_processing_results`, `sky_subtraction`, `flux_calibration`, `detector_map`**
  (PIPE2D-1385).
- **`data_qa.qa_version`, `qa_type`** (PIPE2D-1385).
