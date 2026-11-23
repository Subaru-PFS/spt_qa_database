"""PIPE2D-1677: slit_offset_confirmed, the per-run cross-arm slit-offset outliers

slit_offset_confirmed: drp_qa's metrics.slitOffsets flags the fibers whose slit offset
is an outlier within its MTP ferrule in two or more arms of a spectrograph, from a run's
detectorMap_calib; drpQa.py redo writes them here, one row per (observing run,
spectrograph, fiber). Keyed by the observing run, not the Butler collection, so a rebuild
or reprocessing replaces a run's rows rather than adding a set; collection_name keeps the
build it came from. The run-to-run trajectory is read from this table. Version 0.8.0.

Revision ID: b2d4f6a8c019
Revises: 3f9b7c1e5a24
Create Date: 2026-11-22 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2d4f6a8c019'
down_revision: Union[str, None] = '3f9b7c1e5a24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'slit_offset_confirmed',
        sa.Column('slit_offset_confirmed_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('run', sa.String(), nullable=False, comment='the observing run, e.g. run31 (the key)'),
        sa.Column('collection_name', sa.String(), nullable=False,
                  comment='the detectorMap_calib collection the offsets came from (provenance)'),
        sa.Column('spectrograph', sa.Integer(), nullable=False),
        sa.Column('fiber_id', sa.Integer(), nullable=False),
        sa.Column('n_arms', sa.Integer(), nullable=False,
                  comment='arms of the spectrograph the fiber is an outlier in (>=2)'),
        sa.Column('arms', sa.String(), nullable=False, comment='those arms, e.g. b,m,n,r'),
        sa.Column('max_spatial_resid', sa.Float(precision=53), nullable=True,
                  comment='largest |spatial offset - MTP median| over the arms, pixels'),
        sa.Column('max_spectral_resid', sa.Float(precision=53), nullable=True,
                  comment='largest |spectral offset - MTP median| over the arms, pixels'),
        sa.Column('created_at', sa.DateTime(), nullable=True, comment='when the row was written'),
        sa.PrimaryKeyConstraint('slit_offset_confirmed_id'),
        sa.UniqueConstraint('run', 'spectrograph', 'fiber_id', name='uq_slit_offset_confirmed'),
    )
    op.create_index(op.f('ix_slit_offset_confirmed_run'), 'slit_offset_confirmed', ['run'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_slit_offset_confirmed_run'), table_name='slit_offset_confirmed')
    op.drop_table('slit_offset_confirmed')
