"""PIPE2D-2013: the QA redesign: one verdict per image, normal values, no thresholds tables

The tasks measure and the gate alone judges (drp_qa 0.5.0), so the numbers
tables hold no verdict and nothing records a thresholds file.

Added: qa_normal_value, each camera's normal values, which the gate's percentage
checks compare with; detector_health_qa, the reduction's detector statistics
per amplifier, long format; n_saturated_lines and pct_saturated_pixels on
image_quality_qa; frame_type on qa_gate; and, for the frame classification
(PIPE2D-2015), seq_type on image_quality_qa and dm_line_residual_qa and lamps on
image_quality_qa, null on the rows already there.

Dropped: qa_thresholds, qa_threshold_entry and qa_processing_thresholds; the
verdict columns of image_quality_qa, dm_line_residual_qa and twilight_qa
(qa_status, qa_decided_by, qa_reason), status of dm_line_residual_qa_metric and
recommended_action of dm_line_residual_qa; decided_by_task and provisional of
qa_gate.

The numbers the gate reads become double precision, so a number judged again
from the database is the one judged at load. A value already stored keeps its
single-precision digits.

Rows: every measured number stays, and so does every qa_gate row, with
frame_type null for a verdict of the earlier gate. What the dropped columns and
tables held is not copied: take a dump first. The downgrade restores the schema,
not those rows. Version 0.6.0.

Revision ID: c9e4f2a6d813
Revises: acbd1a9681d6
Create Date: 2026-11-19 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9e4f2a6d813'
down_revision: Union[str, None] = 'acbd1a9681d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_GATE_READS = 'double precision: the gate reads it'

#: The numbers the gate reads, as (table, column, comment): single precision before, double after.
_DOUBLES = (
    ('image_quality_qa', 'med_fwhm', 'median FWHM [pix]'),
    ('image_quality_qa', 'med_dx_center', 'median spatial offset from detectorMap_calib [pix]'),
    ('image_quality_qa', 'lines_per_fiber', 'unflagged lamp lines (trace centroids on a quartz) per lit fiber'),
    ('dm_line_residual_qa_metric', 'value', None),
    ('twilight_qa', 'twilight_level_offset',
     "the detector's level against the sequence's, over the field's [%]; null with no measured fiber or no reference"),
    ('twilight_qa', 'twilight_resid_rms',
     "field RMS beyond photon noise against the sequence's other bright exposures [%]"),
    ('twilight_qa', 'twilight_patch',
     "deepest coherent deviation: largest |median| over a fiber's nearest neighbours [%]"),
)

_STATUS = 'PASS, WARN, FAIL or UNKNOWN'
_DECIDED_BY = 'the metric that decided a WARN or FAIL'
_TWILIGHT_STATUS = ("PASS, WARN or FAIL: the worst of the detector's level offset and its arm's RMS and patch;"
                    " UNKNOWN for an arm the thresholds leave out (n)")

#: The verdict columns the numbers tables lose, as (table, column, comment), in the order the downgrade adds them.
_VERDICTS = (
    ('image_quality_qa', 'qa_status', _STATUS),
    ('image_quality_qa', 'qa_decided_by', _DECIDED_BY),
    ('image_quality_qa', 'qa_reason', None),
    ('dm_line_residual_qa', 'qa_status', _STATUS),
    ('dm_line_residual_qa', 'qa_decided_by', None),
    ('dm_line_residual_qa', 'qa_reason', None),
    ('dm_line_residual_qa', 'recommended_action',
     'NOMINAL, APPLY_SHIFT, RECALIBRATE, INSUFFICIENT_DATA or UNJUDGED'),
    ('dm_line_residual_qa_metric', 'status', 'PASS, WARN or FAIL; empty when not judged'),
    ('twilight_qa', 'qa_status', _TWILIGHT_STATUS),
    ('twilight_qa', 'qa_decided_by', _DECIDED_BY),
    ('twilight_qa', 'qa_reason', None),
)

_FRAME_TYPE = ('the frame type judged: science, allsky, arc, quartz, twilight, iisArc or iisQuartz;'
               ' null for a frame with no type, and for a verdict of the gate before the redesign')

_SEQ_TYPE = "the raw sequence type (W_SEQTYP; the opdb's iic_sequence.sequence_type), e.g. scienceArc, darks, fiberProfiles"
_LAMPS = ('the lamps the header says were lit, as obs_pfs getLamps names them, sorted and joined with +,'
          ' e.g. HgAr+Ne; empty when none')

#: What the frame classification reads, as (table, column, comment).
_CLASSIFICATION = (
    ('image_quality_qa', 'seq_type', _SEQ_TYPE),
    ('image_quality_qa', 'lamps', _LAMPS),
    ('dm_line_residual_qa', 'seq_type', _SEQ_TYPE),
)

#: qa_gate comments that change, as (column, before, after).
_GATE_COMMENTS = (
    ('qa_decided_by', _DECIDED_BY, 'the check that decided a WARN or FAIL'),
    ('qa_reason', 'every task reason, prefixed by its task', 'the check, the value and the limit crossed'),
)


def _joined(comment, extra):
    return f'{comment}; {extra}' if comment else extra


def upgrade() -> None:
    op.create_table(
        'qa_normal_value',
        sa.Column('normal_value_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('collection_name', sa.String(), nullable=False,
                  comment='the collection whose frames the value judges'),
        sa.Column('metric', sa.String(), nullable=False),
        sa.Column('camera', sa.String(), nullable=False,
                  comment='a camera, e.g. b1; or an arm for a per-arm value'),
        sa.Column('frame_type', sa.String(), server_default='', nullable=False,
                  comment='the frame type the value is for, as in qa_gate'),
        sa.Column('selector', sa.String(), server_default='', nullable=False,
                  comment='lamp or species; empty when neither applies'),
        sa.Column('valid_from', sa.Integer(), nullable=False, comment='the first visit the value judges'),
        sa.Column('value', sa.Float(precision=53), nullable=False),
        sa.Column('n_frames', sa.Integer(), nullable=False, comment='exposures the value rests on'),
        sa.Column('source_visits', sa.String(), nullable=True, comment='the visits it was made from'),
        sa.Column('accepted_by', sa.String(), nullable=True),
        sa.Column('accepted_at', sa.DateTime(), nullable=True),
        sa.Column('reason', sa.String(), nullable=True, comment='why a value beyond the limits was accepted'),
        sa.PrimaryKeyConstraint('normal_value_id'),
        sa.UniqueConstraint('collection_name', 'metric', 'camera', 'frame_type', 'selector', 'valid_from',
                            name='uq_normal_value'),
    )
    op.create_table(
        'detector_health_qa',
        sa.Column('processing_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('pfs_visit_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('camera_name', sa.String(length=2), autoincrement=False, nullable=False,
                  comment='arm and spectrograph, e.g. b1'),
        sa.Column('amplifier', sa.String(), server_default='', autoincrement=False, nullable=False,
                  comment='amplifier name; empty for a statistic of the whole detector (the n arm)'),
        sa.Column('metric', sa.String(), autoincrement=False, nullable=False),
        sa.Column('value', sa.Float(precision=53), nullable=True,
                  comment='double precision: pixel counts are stored exactly'),
        sa.ForeignKeyConstraint(['pfs_visit_id'], ['pfs_visit.pfs_visit_id']),
        sa.ForeignKeyConstraint(['processing_id'], ['data_processing_pipe2d.processing_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('processing_id', 'pfs_visit_id', 'camera_name', 'amplifier', 'metric'),
    )
    op.create_index(op.f('ix_detector_health_qa_pfs_visit_id'), 'detector_health_qa', ['pfs_visit_id'],
                    unique=False)

    op.add_column('image_quality_qa',
                  sa.Column('n_saturated_lines', sa.Integer(), nullable=True,
                            comment='lamp or sky lines saturated at their expected position (the SAT mask plane of the calexp)'))
    op.add_column('image_quality_qa',
                  sa.Column('pct_saturated_pixels', sa.REAL(), nullable=True,
                            comment="per cent of the pixels within the lit fibers' apertures that are saturated"))
    op.add_column('qa_gate', sa.Column('frame_type', sa.String(), nullable=True, comment=_FRAME_TYPE))
    for table, column, comment in _CLASSIFICATION:
        op.add_column(table, sa.Column(column, sa.String(), nullable=True, comment=comment))

    for table, column, _ in _VERDICTS:
        op.drop_column(table, column)
    op.drop_column('qa_gate', 'decided_by_task')
    op.drop_column('qa_gate', 'provisional')
    for column, before, after in _GATE_COMMENTS:
        op.alter_column('qa_gate', column, existing_type=sa.String(), comment=after, existing_comment=before)

    for table, column, comment in _DOUBLES:
        op.alter_column(table, column, existing_type=sa.REAL(), type_=sa.Float(precision=53),
                        existing_comment=comment, comment=_joined(comment, _GATE_READS))

    op.drop_index(op.f('ix_qa_processing_thresholds_thresholds_id'), table_name='qa_processing_thresholds')
    op.drop_table('qa_processing_thresholds')
    op.drop_table('qa_threshold_entry')
    op.drop_table('qa_thresholds')


def downgrade() -> None:
    op.create_table(
        'qa_thresholds',
        sa.Column('thresholds_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sha256', sa.String(length=64), nullable=False,
                  comment='of the file: the same thresholds registered twice are one row'),
        sa.Column('name', sa.String(), nullable=True,
                  comment='file name, e.g. iqQaThresholds-run25.yaml; <task>.config for a config layer'),
        sa.Column('derived_on', sa.DateTime(), nullable=True,
                  comment='the day the thresholds were derived (the file says the date alone)'),
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
        sa.Column('illumination', sa.String(), nullable=True,
                  comment='null means the default, full: an entry that names no illumination judges PFI frames alone (drp_qa gate.DEFAULT_POPULATION)'),
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
        'qa_processing_thresholds',
        sa.Column('processing_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('task', sa.String(), autoincrement=False, nullable=False,
                  comment='imageQualityQa, dmLineResiduals or twilightQa'),
        sa.Column('layer', sa.Integer(), autoincrement=False, nullable=False,
                  comment='position in the order judged, from 0; a layer that could not be cited leaves a gap'),
        sa.Column('thresholds_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['processing_id'], ['data_processing_pipe2d.processing_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['thresholds_id'], ['qa_thresholds.thresholds_id']),
        sa.PrimaryKeyConstraint('processing_id', 'task', 'layer'),
    )
    op.create_index(op.f('ix_qa_processing_thresholds_thresholds_id'), 'qa_processing_thresholds',
                    ['thresholds_id'], unique=False)

    # Back to single precision: a number stored since the upgrade is rounded.
    for table, column, comment in _DOUBLES:
        op.alter_column(table, column, existing_type=sa.Float(precision=53), type_=sa.REAL(),
                        existing_comment=_joined(comment, _GATE_READS), comment=comment)

    for column, before, after in _GATE_COMMENTS:
        op.alter_column('qa_gate', column, existing_type=sa.String(), comment=before, existing_comment=after)
    op.add_column('qa_gate',
                  sa.Column('provisional', sa.Boolean(), nullable=True,
                            comment='the reduction pipeline differs from the thresholds (gate.pipelineMismatch)'))
    op.add_column('qa_gate',
                  sa.Column('decided_by_task', sa.String(), nullable=True,
                            comment='imageQualityQa, dmLineResiduals or twilightQa'))
    for table, column, comment in _VERDICTS:
        op.add_column(table, sa.Column(column, sa.String(), nullable=True, comment=comment))

    for table, column, _ in reversed(_CLASSIFICATION):
        op.drop_column(table, column)
    op.drop_column('qa_gate', 'frame_type')
    op.drop_column('image_quality_qa', 'pct_saturated_pixels')
    op.drop_column('image_quality_qa', 'n_saturated_lines')
    op.drop_index(op.f('ix_detector_health_qa_pfs_visit_id'), table_name='detector_health_qa')
    op.drop_table('detector_health_qa')
    op.drop_table('qa_normal_value')
