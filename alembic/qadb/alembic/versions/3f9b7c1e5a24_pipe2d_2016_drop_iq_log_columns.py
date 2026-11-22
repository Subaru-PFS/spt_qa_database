"""PIPE2D-2016: drop image_quality_qa's log-scraped columns

imageQualityQa no longer parses the ISR, cosmic-ray and reduceExposure logs
(drp_qa, PIPE2D-2016): the detectorMap fit scalars and the ISR/cosmic-ray counts
are read from the reduction's task metadata and stored in detector_health_qa
(reductionStats, PIPE2D-2013/2014), and the per-species fit statistics come from
reduceExposure_metadata into image_quality_qa_species. The task-timing columns had
no other source and are not kept.

Dropped from image_quality_qa: isr_bad_pixels, isr_time, cosmic_ray_count,
cosmic_ray_pixels, cosmic_ray_time, reduce_exposure_time, fit_chi2, fit_dof,
fit_x_rms, fit_y_rms, fit_x_soften, fit_y_soften, fit_n_lines, fit_total_lines,
fit_reserved_chi2, fit_reserved_x_rms, fit_reserved_y_rms, fit_reserved_x_soften,
fit_reserved_y_soften, fit_reserved_n_lines.

Apply this only after the drp_qa release that stops writing these columns is
deployed: an earlier loader still upserts them. The downgrade restores the schema
(nullable columns), not the values the drop removed; take a dump first. Version 0.7.0.

Revision ID: 3f9b7c1e5a24
Revises: c9e4f2a6d813
Create Date: 2026-11-21 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3f9b7c1e5a24'
down_revision: Union[str, None] = 'c9e4f2a6d813'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_SECONDS = '[s]'
_PIXELS = '[pix]'

#: The log-scraped columns to drop, with the type and comment to restore on downgrade.
_COLUMNS = (
    ('isr_bad_pixels', sa.Integer(), None),
    ('isr_time', sa.REAL(), _SECONDS),
    ('cosmic_ray_count', sa.Integer(), None),
    ('cosmic_ray_pixels', sa.Integer(), None),
    ('cosmic_ray_time', sa.REAL(), _SECONDS),
    ('reduce_exposure_time', sa.REAL(), _SECONDS),
    ('fit_chi2', sa.REAL(), 'detectorMap fit, from the reduceExposure log'),
    ('fit_dof', sa.Integer(), None),
    ('fit_x_rms', sa.REAL(), _PIXELS),
    ('fit_y_rms', sa.REAL(), _PIXELS),
    ('fit_x_soften', sa.REAL(), _PIXELS),
    ('fit_y_soften', sa.REAL(), _PIXELS),
    ('fit_n_lines', sa.Integer(), None),
    ('fit_total_lines', sa.Integer(), None),
    ('fit_reserved_chi2', sa.REAL(), None),
    ('fit_reserved_x_rms', sa.REAL(), _PIXELS),
    ('fit_reserved_y_rms', sa.REAL(), _PIXELS),
    ('fit_reserved_x_soften', sa.REAL(), _PIXELS),
    ('fit_reserved_y_soften', sa.REAL(), _PIXELS),
    ('fit_reserved_n_lines', sa.Integer(), None),
)


def upgrade() -> None:
    for column, _type, _comment in _COLUMNS:
        op.drop_column('image_quality_qa', column)


def downgrade() -> None:
    for column, type_, comment in _COLUMNS:
        op.add_column(
            'image_quality_qa', sa.Column(column, type_, nullable=True, comment=comment)
        )
