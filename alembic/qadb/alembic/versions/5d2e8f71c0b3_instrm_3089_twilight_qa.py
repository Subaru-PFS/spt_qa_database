"""INSTRM-3089: the twilight sequence check in the per-image gate

twilight_qa: drp_qa's twilightQa.py judges each exposure of a twilight sequence
against the sequence's others once it is complete (PIPE2D-1973) and stores the
verdict per detector image in the Butler (twilightQaMetrics); the qadb loader
copies it here, keyed by the processing like image_quality_qa, and folds it into
qa_gate as a third task, twilightQa, citing the thresholds file it judged with
(qa_gate.twilight_thresholds_id). Version 0.3.0.

Revision ID: 5d2e8f71c0b3
Revises: a7c3e5d91b24
Create Date: 2026-11-04 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d2e8f71c0b3'
down_revision: Union[str, None] = 'a7c3e5d91b24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'twilight_qa',
        sa.Column('processing_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('pfs_visit_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('camera_name', sa.String(length=2), autoincrement=False, nullable=False,
                  comment='arm and spectrograph, e.g. b1'),
        sa.Column('spectrograph', sa.Integer(), nullable=True),
        sa.Column('arm', sa.String(length=1), nullable=True),
        sa.Column('iic_sequence_id', sa.Integer(), nullable=True,
                  comment='the IIC sequence judged (opdb iic_sequence; W_SEQID)'),
        sa.Column('seq_name', sa.String(), nullable=True, comment='W_SEQNAM'),
        sa.Column('n_exposures', sa.Integer(), nullable=True, comment='exposures of the sequence in this arm'),
        sa.Column('snr', sa.REAL(), nullable=True, comment='median S/N per pixel of the exposure in this arm'),
        sa.Column('brightness', sa.REAL(), nullable=True,
                  comment='median S/N per pixel of the exposure in the brightness arm (b)'),
        sa.Column('too_faint', sa.Boolean(), nullable=True,
                  comment='below the brightness floor: not a good flat; the RMS is not measured'),
        sa.Column('n_reference', sa.Integer(), nullable=True,
                  comment='bright exposures in the reference median, this one included; 0 when the RMS is not measured'),
        sa.Column('noise', sa.REAL(), nullable=True, comment='photon noise expected in the RMS [%]'),
        sa.Column('sat_fraction', sa.REAL(), nullable=True,
                  comment="largest saturated fraction of a fiber's window on the detector"),
        sa.Column('n_measured', sa.Integer(), nullable=True,
                  comment='fibers of the detector with a measured flux in this exposure'),
        sa.Column('twilight_level_offset', sa.REAL(), nullable=True,
                  comment="the detector's level against the sequence's, over the field's [%]; null with no measured fiber or no reference"),
        sa.Column('twilight_resid_rms', sa.REAL(), nullable=True,
                  comment="field RMS beyond photon noise against the sequence's other bright exposures [%]"),
        sa.Column('twilight_patch', sa.REAL(), nullable=True,
                  comment="deepest coherent deviation: largest |median| over a fiber's nearest neighbours [%]"),
        sa.Column('twilight_arm_mean', sa.REAL(), nullable=True,
                  comment="RMS of the mean of each fiber's b and r residuals [%]"),
        sa.Column('twilight_arm_half_diff', sa.REAL(), nullable=True,
                  comment="RMS of half the difference of each fiber's b and r residuals [%]"),
        sa.Column('qa_status', sa.String(), nullable=True,
                  comment="PASS, WARN or FAIL: the worst of the detector's level offset and its arm's RMS and patch; UNKNOWN for an arm the thresholds leave out (n)"),
        sa.Column('qa_decided_by', sa.String(), nullable=True, comment='the metric that decided a WARN or FAIL'),
        sa.Column('qa_reason', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['processing_id'], ['data_processing_pipe2d.processing_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pfs_visit_id'], ['pfs_visit.pfs_visit_id']),
        sa.PrimaryKeyConstraint('processing_id', 'pfs_visit_id', 'camera_name'),
    )
    op.create_index(op.f('ix_twilight_qa_pfs_visit_id'), 'twilight_qa', ['pfs_visit_id'], unique=False)
    op.create_index(op.f('ix_twilight_qa_iic_sequence_id'), 'twilight_qa', ['iic_sequence_id'], unique=False)

    op.add_column('qa_gate',
                  sa.Column('twilight_thresholds_id', sa.Integer(), nullable=True,
                            comment='the twilight thresholds file a twilight image was judged with (INSTRM-3089)'))
    op.create_foreign_key(op.f('fk_qa_gate_twilight_thresholds_id_qa_thresholds'), 'qa_gate', 'qa_thresholds',
                          ['twilight_thresholds_id'], ['thresholds_id'])
    op.alter_column('qa_gate', 'decided_by_task', comment='imageQualityQa, dmLineResiduals or twilightQa',
                    existing_type=sa.String(), existing_comment='imageQualityQa or dmLineResiduals')


def downgrade() -> None:
    op.alter_column('qa_gate', 'decided_by_task', comment='imageQualityQa or dmLineResiduals',
                    existing_type=sa.String(), existing_comment='imageQualityQa, dmLineResiduals or twilightQa')
    op.drop_constraint(op.f('fk_qa_gate_twilight_thresholds_id_qa_thresholds'), 'qa_gate', type_='foreignkey')
    op.drop_column('qa_gate', 'twilight_thresholds_id')
    op.drop_index(op.f('ix_twilight_qa_iic_sequence_id'), table_name='twilight_qa')
    op.drop_index(op.f('ix_twilight_qa_pfs_visit_id'), table_name='twilight_qa')
    op.drop_table('twilight_qa')
