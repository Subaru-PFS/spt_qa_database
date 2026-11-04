"""INSTRM-3089: twilight sequence verdicts

twilight_qa (per exposure and arm: PASS, WARN, FAIL or TOO_FAINT with the reasons) and
twilight_qa_metric (the measurements per detector image), written by drp_qa's
bin.src/twilightQa.py once a twilight sequence is complete (PIPE2D-1973), from
ics_qaActor after each visit's QA. Version 0.3.0.

Revision ID: 5d2e8f71c0b3
Revises: a7c3e5d91b24
Create Date: 2026-11-03 12:00:00.000000

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
        sa.Column('pfs_visit_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('arm', sa.String(length=1), autoincrement=False, nullable=False),
        sa.Column('iic_sequence_id', sa.Integer(), nullable=True,
                  comment='the IIC sequence judged (opdb iic_sequence)'),
        sa.Column('qa_status', sa.String(), nullable=True,
                  comment='PASS, WARN, FAIL or TOO_FAINT (below the brightness floor: not a flat)'),
        sa.Column('qa_reason', sa.String(), nullable=True,
                  comment='the WARN and FAIL reasons, ;-joined; empty on a PASS'),
        sa.Column('twilight_arm_mean', sa.REAL(), nullable=True,
                  comment="RMS of the mean of each fiber's b and r residuals [%]"),
        sa.Column('twilight_arm_half_diff', sa.REAL(), nullable=True,
                  comment="RMS of half the difference of each fiber's b and r residuals [%]"),
        sa.Column('collection_name', sa.String(), nullable=True,
                  comment='the collection the twilightFiberFlux tables were read from'),
        sa.Column('drp_qa_version', sa.String(), nullable=True, comment='the drp_qa that judged'),
        sa.Column('judged_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['pfs_visit_id'], ['pfs_visit.pfs_visit_id']),
        sa.PrimaryKeyConstraint('pfs_visit_id', 'arm'),
    )
    op.create_index(op.f('ix_twilight_qa_pfs_visit_id'), 'twilight_qa', ['pfs_visit_id'], unique=False)
    op.create_index(op.f('ix_twilight_qa_iic_sequence_id'), 'twilight_qa', ['iic_sequence_id'], unique=False)

    op.create_table(
        'twilight_qa_metric',
        sa.Column('pfs_visit_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('camera_name', sa.String(length=2), autoincrement=False, nullable=False,
                  comment='arm and spectrograph, e.g. b1'),
        sa.Column('spectrograph', sa.Integer(), nullable=True),
        sa.Column('arm', sa.String(length=1), nullable=True),
        sa.Column('iic_sequence_id', sa.Integer(), nullable=True,
                  comment='the IIC sequence judged (opdb iic_sequence)'),
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
        sa.ForeignKeyConstraint(['pfs_visit_id'], ['pfs_visit.pfs_visit_id']),
        sa.PrimaryKeyConstraint('pfs_visit_id', 'camera_name'),
    )
    op.create_index(op.f('ix_twilight_qa_metric_pfs_visit_id'), 'twilight_qa_metric', ['pfs_visit_id'],
                    unique=False)
    op.create_index(op.f('ix_twilight_qa_metric_iic_sequence_id'), 'twilight_qa_metric', ['iic_sequence_id'],
                    unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_twilight_qa_metric_iic_sequence_id'), table_name='twilight_qa_metric')
    op.drop_index(op.f('ix_twilight_qa_metric_pfs_visit_id'), table_name='twilight_qa_metric')
    op.drop_table('twilight_qa_metric')
    op.drop_index(op.f('ix_twilight_qa_iic_sequence_id'), table_name='twilight_qa')
    op.drop_index(op.f('ix_twilight_qa_pfs_visit_id'), table_name='twilight_qa')
    op.drop_table('twilight_qa')
