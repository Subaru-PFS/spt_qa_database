"""PIPE2D-1385: per-image gate tables

image_quality_qa (+ _species), dm_line_residual_qa (+ _metric), qa_thresholds
(+ qa_threshold_entry) and qa_gate, loaded from the Butler by drp_qa's
pfs.drp.qa.qadb; data_processing_pipe2d gains the reduction's datamodel and
obs_pfs versions. detector_map_qa, shaped for the retired dmResiduals task and
never written, is dropped: dm_line_residual_qa(_metric) replaces it.

Revision ID: a7c3e5d91b24
Revises: 348db3f79d46
Create Date: 2026-10-26 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7c3e5d91b24'
down_revision: Union[str, None] = '348db3f79d46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _image_keys():
    return [
        sa.Column('processing_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('pfs_visit_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('camera_name', sa.String(length=2), autoincrement=False, nullable=False,
                  comment='arm and spectrograph, e.g. b1'),
    ]


def upgrade() -> None:
    op.drop_table('detector_map_qa')
    op.add_column('data_processing_pipe2d',
                  sa.Column('datamodel_version', sa.String(), nullable=True,
                            comment='datamodel version of the reduction (e.g., w.2026.40)'))
    op.add_column('data_processing_pipe2d',
                  sa.Column('obs_pfs_version', sa.String(), nullable=True,
                            comment='obs_pfs version of the reduction (e.g., w.2026.40)'))

    op.create_table(
        'image_quality_qa',
        *_image_keys(),
        sa.Column('spectrograph', sa.Integer(), nullable=True),
        sa.Column('arm', sa.String(length=1), nullable=True),
        sa.Column('obs_type', sa.String(), nullable=True,
                  comment='frame type from W_SEQTYP: arc, trace, object, twilight, dark, ...'),
        sa.Column('seq_name', sa.String(), nullable=True, comment='W_SEQNAM'),
        sa.Column('trace_only', sa.Boolean(), nullable=True,
                  comment='FWHM read from the fiberProfiles calibration, not measured'),
        sa.Column('med_fwhm', sa.REAL(), nullable=True, comment='median FWHM [pix]'),
        sa.Column('med_dx_center', sa.REAL(), nullable=True,
                  comment='median spatial offset from detectorMap_calib [pix]'),
        sa.Column('dx_center_rms', sa.REAL(), nullable=True, comment='RMS of the spatial offset [pix]'),
        sa.Column('pct_flagged', sa.REAL(), nullable=True, comment='per cent of lines flagged'),
        sa.Column('pct_low_sn', sa.REAL(), nullable=True, comment='per cent of lines flagged for low S/N'),
        sa.Column('pct_meas_fail', sa.REAL(), nullable=True,
                  comment='per cent of lines whose measurement failed'),
        sa.Column('n_lines', sa.Integer(), nullable=True, comment='rows of lines'),
        sa.Column('lines_per_fiber', sa.REAL(), nullable=True,
                  comment='unflagged lamp lines (trace centroids on a quartz) per lit fiber'),
        sa.Column('n_lit_fibers', sa.Integer(), nullable=True,
                  comment='fibers of the detector the pfsConfig lights'),
        sa.Column('n_fibers', sa.Integer(), nullable=True,
                  comment='fibers of the detector lit or behind a black dot'),
        sa.Column('n_trace_rows', sa.Integer(), nullable=True, comment='trace centroids in lines'),
        sa.Column('qa_status', sa.String(), nullable=True, comment='PASS, WARN, FAIL or UNKNOWN'),
        sa.Column('qa_decided_by', sa.String(), nullable=True,
                  comment='the metric that decided a WARN or FAIL'),
        sa.Column('qa_reason', sa.String(), nullable=True),
        sa.Column('calexp_run', sa.String(), nullable=True, comment='Butler RUN of the calexp judged'),
        sa.Column('isr_bad_pixels', sa.Integer(), nullable=True),
        sa.Column('isr_time', sa.REAL(), nullable=True, comment='[s]'),
        sa.Column('cosmic_ray_count', sa.Integer(), nullable=True),
        sa.Column('cosmic_ray_pixels', sa.Integer(), nullable=True),
        sa.Column('cosmic_ray_time', sa.REAL(), nullable=True, comment='[s]'),
        sa.Column('reduce_exposure_time', sa.REAL(), nullable=True, comment='[s]'),
        sa.Column('fit_chi2', sa.REAL(), nullable=True,
                  comment='detectorMap fit, from the reduceExposure log'),
        sa.Column('fit_dof', sa.Integer(), nullable=True),
        sa.Column('fit_x_rms', sa.REAL(), nullable=True, comment='[pix]'),
        sa.Column('fit_y_rms', sa.REAL(), nullable=True, comment='[pix]'),
        sa.Column('fit_x_soften', sa.REAL(), nullable=True, comment='[pix]'),
        sa.Column('fit_y_soften', sa.REAL(), nullable=True, comment='[pix]'),
        sa.Column('fit_n_lines', sa.Integer(), nullable=True),
        sa.Column('fit_total_lines', sa.Integer(), nullable=True),
        sa.Column('fit_reserved_chi2', sa.REAL(), nullable=True),
        sa.Column('fit_reserved_x_rms', sa.REAL(), nullable=True, comment='[pix]'),
        sa.Column('fit_reserved_y_rms', sa.REAL(), nullable=True, comment='[pix]'),
        sa.Column('fit_reserved_x_soften', sa.REAL(), nullable=True, comment='[pix]'),
        sa.Column('fit_reserved_y_soften', sa.REAL(), nullable=True, comment='[pix]'),
        sa.Column('fit_reserved_n_lines', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['pfs_visit_id'], ['pfs_visit.pfs_visit_id']),
        sa.ForeignKeyConstraint(['processing_id'], ['data_processing_pipe2d.processing_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('processing_id', 'pfs_visit_id', 'camera_name'),
    )
    op.create_table(
        'image_quality_qa_species',
        *_image_keys(),
        sa.Column('description', sa.String(), autoincrement=False, nullable=False,
                  comment='line species, Trace included'),
        sa.Column('metric', sa.String(), autoincrement=False, nullable=False,
                  comment='fitXRms, fitYRms, fitXSoften, fitYSoften'),
        sa.Column('value', sa.REAL(), nullable=True),
        sa.ForeignKeyConstraint(
            ['processing_id', 'pfs_visit_id', 'camera_name'],
            ['image_quality_qa.processing_id', 'image_quality_qa.pfs_visit_id',
             'image_quality_qa.camera_name'],
            ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('processing_id', 'pfs_visit_id', 'camera_name', 'description', 'metric'),
    )
    op.create_table(
        'dm_line_residual_qa',
        *_image_keys(),
        sa.Column('spectrograph', sa.Integer(), nullable=True),
        sa.Column('arm', sa.String(length=1), nullable=True),
        sa.Column('camera_set', sa.String(), nullable=True,
                  comment='the arms the pfsConfig exposed, e.g. brn'),
        sa.Column('obs_type', sa.String(), nullable=True),
        sa.Column('fitted', sa.Boolean(), nullable=True,
                  comment='false when the visit detectorMap fit marked no line'),
        sa.Column('n_species', sa.Integer(), nullable=True),
        sa.Column('n_species_measured', sa.Integer(), nullable=True),
        sa.Column('qa_status', sa.String(), nullable=True, comment='PASS, WARN, FAIL or UNKNOWN'),
        sa.Column('qa_decided_by', sa.String(), nullable=True),
        sa.Column('qa_reason', sa.String(), nullable=True),
        sa.Column('recommended_action', sa.String(), nullable=True,
                  comment='NOMINAL, APPLY_SHIFT, RECALIBRATE, INSUFFICIENT_DATA or UNJUDGED'),
        sa.Column('calib_id', sa.String(), nullable=True,
                  comment='Butler dataset id of the detectorMap_calib'),
        sa.Column('calib_run', sa.String(), nullable=True, comment='Butler RUN of the detectorMap_calib'),
        sa.Column('calib_created', sa.String(), nullable=True,
                  comment='CALIB_CREATION_DATE of the detectorMap_calib'),
        sa.Column('calib_first_visit', sa.Integer(), nullable=True),
        sa.Column('calib_last_visit', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['pfs_visit_id'], ['pfs_visit.pfs_visit_id']),
        sa.ForeignKeyConstraint(['processing_id'], ['data_processing_pipe2d.processing_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('processing_id', 'pfs_visit_id', 'camera_name'),
    )
    op.create_table(
        'dm_line_residual_qa_metric',
        *_image_keys(),
        sa.Column('reference', sa.String(), autoincrement=False, nullable=False,
                  comment='calib: detectorMap_calib; visit: the visit detectorMap'),
        sa.Column('description', sa.String(), autoincrement=False, nullable=False,
                  comment='line species, Trace included'),
        sa.Column('status_type', sa.String(), autoincrement=False, nullable=False,
                  comment='BOTH, USED, RESERVED or UNFITTED'),
        sa.Column('metric', sa.String(), autoincrement=False, nullable=False,
                  comment='nLines, linesPerFiber, medianDeltaX, robustRmsDeltaX, medianDeltaY, robustRmsDeltaY'),
        sa.Column('value', sa.REAL(), nullable=True),
        sa.Column('status', sa.String(), nullable=True,
                  comment='PASS, WARN or FAIL; empty when not judged'),
        sa.ForeignKeyConstraint(
            ['processing_id', 'pfs_visit_id', 'camera_name'],
            ['dm_line_residual_qa.processing_id', 'dm_line_residual_qa.pfs_visit_id',
             'dm_line_residual_qa.camera_name'],
            ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('processing_id', 'pfs_visit_id', 'camera_name', 'reference',
                                'description', 'status_type', 'metric'),
    )
    op.create_table(
        'qa_thresholds',
        sa.Column('thresholds_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sha256', sa.String(length=64), nullable=False,
                  comment='of the file: the same thresholds registered twice are one row'),
        sa.Column('name', sa.String(), nullable=True, comment='file name, e.g. iqQaThresholds-run25.yaml'),
        sa.Column('derived_on', sa.String(), nullable=True, comment='YYYY-MM-DD'),
        sa.Column('collection', sa.String(), nullable=True,
                  comment='the collection the thresholds were derived from'),
        sa.Column('reference_runs', sa.String(), nullable=True, comment='comma-separated, e.g. 25,29'),
        sa.Column('drp_qa_version', sa.String(), nullable=True),
        sa.Column('datamodel_version', sa.String(), nullable=True),
        sa.Column('obs_pfs_version', sa.String(), nullable=True),
        sa.Column('drp_stella_version', sa.String(), nullable=True),
        sa.Column('n_entries', sa.Integer(), nullable=True),
        sa.Column('registered_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('thresholds_id'),
        sa.UniqueConstraint('sha256', name='uq_qa_thresholds_sha256'),
    )
    op.create_table(
        'qa_threshold_entry',
        sa.Column('thresholds_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('metric', sa.String(), autoincrement=False, nullable=False),
        sa.Column('population', sa.String(), autoincrement=False, nullable=False,
                  comment='the population as key=value pairs, e.g. arm=b obsType=arc'),
        sa.Column('arm', sa.String(length=1), nullable=True),
        sa.Column('spectrograph', sa.Integer(), nullable=True),
        sa.Column('obs_type', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('camera_set', sa.String(), nullable=True),
        sa.Column('reference', sa.String(), nullable=True),
        sa.Column('status_type', sa.String(), nullable=True),
        sa.Column('higher_is_worse', sa.Boolean(), nullable=True),
        sa.Column('absolute', sa.Boolean(), nullable=True),
        sa.Column('method', sa.String(), nullable=True, comment='percentile or tolerance'),
        sa.Column('warn', sa.Float(precision=53), nullable=True,
                  comment='double precision: the file value exactly'),
        sa.Column('fail', sa.Float(precision=53), nullable=True,
                  comment='double precision: the file value exactly'),
        sa.Column('n_good', sa.Integer(), nullable=True),
        sa.Column('n_good_visits', sa.Integer(), nullable=True),
        sa.Column('visit_range', sa.String(), nullable=True),
        sa.Column('reliable', sa.Boolean(), nullable=True),
        sa.Column('fail_bounded', sa.Boolean(), nullable=True),
        sa.Column('degenerate', sa.Boolean(), nullable=True),
        sa.Column('provenance', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['thresholds_id'], ['qa_thresholds.thresholds_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('thresholds_id', 'metric', 'population'),
    )
    op.create_table(
        'qa_gate',
        *_image_keys(),
        sa.Column('qa_status', sa.String(), nullable=True, comment='PASS, WARN, FAIL or UNKNOWN'),
        sa.Column('decided_by_task', sa.String(), nullable=True,
                  comment='imageQualityQa or dmLineResiduals'),
        sa.Column('qa_decided_by', sa.String(), nullable=True,
                  comment='the metric that decided a WARN or FAIL'),
        sa.Column('qa_reason', sa.String(), nullable=True,
                  comment='every task reason, prefixed by its task'),
        sa.Column('provisional', sa.Boolean(), nullable=True,
                  comment='the reduction pipeline differs from the thresholds (gate.pipelineMismatch)'),
        sa.Column('mode', sa.String(), nullable=True, comment='realtime, comparison or backfill'),
        sa.Column('iq_thresholds_id', sa.Integer(), nullable=True),
        sa.Column('dm_thresholds_id', sa.Integer(), nullable=True),
        sa.Column('decided_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['dm_thresholds_id'], ['qa_thresholds.thresholds_id']),
        sa.ForeignKeyConstraint(['iq_thresholds_id'], ['qa_thresholds.thresholds_id']),
        sa.ForeignKeyConstraint(['pfs_visit_id'], ['pfs_visit.pfs_visit_id']),
        sa.ForeignKeyConstraint(['processing_id'], ['data_processing_pipe2d.processing_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('processing_id', 'pfs_visit_id', 'camera_name'),
    )

    for table in ('image_quality_qa', 'dm_line_residual_qa', 'qa_gate'):
        op.create_index(f'ix_{table}_pfs_visit_id', table, ['pfs_visit_id'])


def downgrade() -> None:
    op.drop_table('qa_gate')
    op.drop_table('qa_threshold_entry')
    op.drop_table('qa_thresholds')
    op.drop_table('dm_line_residual_qa_metric')
    op.drop_table('dm_line_residual_qa')
    op.drop_table('image_quality_qa_species')
    op.drop_table('image_quality_qa')
    op.drop_column('data_processing_pipe2d', 'obs_pfs_version')
    op.drop_column('data_processing_pipe2d', 'datamodel_version')
    op.create_table(
        'detector_map_qa',
        sa.Column('processing_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('pfs_visit_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('camera_name', sa.String(length=2), autoincrement=False, nullable=False),
        sa.Column('status_type', sa.String(), autoincrement=False, nullable=False),
        sa.Column('description', sa.String(), autoincrement=False, nullable=False),
        sa.Column('spectrograph', sa.Integer(), nullable=True),
        sa.Column('arm', sa.String(length=1), nullable=True),
        sa.Column('observation_reason', sa.String(), nullable=True),
        sa.Column('dof', sa.REAL(), nullable=True),
        sa.Column('chi2x', sa.REAL(), nullable=True),
        sa.Column('chi2y', sa.REAL(), nullable=True),
        sa.Column('spatial_median', sa.REAL(), nullable=True),
        sa.Column('spatial_robust_rms', sa.REAL(), nullable=True),
        sa.Column('spatial_weighted_rms', sa.REAL(), nullable=True),
        sa.Column('spatial_soften_fit', sa.REAL(), nullable=True),
        sa.Column('spatial_dof', sa.REAL(), nullable=True),
        sa.Column('spatial_num_fibers', sa.Integer(), nullable=True),
        sa.Column('spatial_num_lines', sa.Integer(), nullable=True),
        sa.Column('wavelength_median', sa.REAL(), nullable=True),
        sa.Column('wavelength_robust_rms', sa.REAL(), nullable=True),
        sa.Column('wavelength_weighted_rms', sa.REAL(), nullable=True),
        sa.Column('wavelength_soften_fit', sa.REAL(), nullable=True),
        sa.Column('wavelength_dof', sa.REAL(), nullable=True),
        sa.Column('wavelength_num_fibers', sa.Integer(), nullable=True),
        sa.Column('wavelength_num_lines', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['pfs_visit_id'], ['pfs_visit.pfs_visit_id']),
        sa.ForeignKeyConstraint(['processing_id'], ['data_processing_pipe2d.processing_id']),
        sa.PrimaryKeyConstraint('processing_id', 'pfs_visit_id', 'camera_name', 'status_type', 'description'),
    )
