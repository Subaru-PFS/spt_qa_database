"""PIPE2D-1991: cite every thresholds layer an image was judged with

qa_gate_thresholds: one row per image, task and layer, in the order the task
judged them. A task judges each metric by the first of its layers with an entry
for the image's population (its thresholds files, then its config's threshold
fields), and qa_gate cited the first layer alone (iq_thresholds_id,
dm_thresholds_id, twilight_thresholds_id), so a metric a later layer judged (the
medianDeltaX/Y drift rows of dmLineResiduals, judged by the config's fields) had
no stored limits. drp_qa's tasks now record every layer, the config fields
written as a thresholds document with a content hash and registered in
qa_thresholds under the name <task>.config, and its loader writes them here.

The three qa_gate columns go: what they cited becomes each image's layer 0 for
the task, and the new table is the one record. Version 0.4.0.

Revision ID: acbd1a9681d6
Revises: 5d2e8f71c0b3
Create Date: 2026-11-06 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acbd1a9681d6'
down_revision: Union[str, None] = '5d2e8f71c0b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#: The qa_gate column that cited each task's first layer, dropped here.
_FIRST_LAYER = (
    ('imageQualityQa', 'iq_thresholds_id'),
    ('dmLineResiduals', 'dm_thresholds_id'),
    ('twilightQa', 'twilight_thresholds_id'),
)


def upgrade() -> None:
    op.create_table(
        'qa_gate_thresholds',
        sa.Column('processing_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('pfs_visit_id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('camera_name', sa.String(length=2), autoincrement=False, nullable=False,
                  comment='arm and spectrograph, e.g. b1'),
        sa.Column('task', sa.String(), autoincrement=False, nullable=False,
                  comment='imageQualityQa, dmLineResiduals or twilightQa'),
        sa.Column('layer', sa.Integer(), autoincrement=False, nullable=False,
                  comment='position in the order judged, from 0; a layer that could not be cited leaves a gap'),
        sa.Column('thresholds_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['processing_id', 'pfs_visit_id', 'camera_name'],
            ['qa_gate.processing_id', 'qa_gate.pfs_visit_id', 'qa_gate.camera_name'],
            ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['thresholds_id'], ['qa_thresholds.thresholds_id']),
        sa.PrimaryKeyConstraint('processing_id', 'pfs_visit_id', 'camera_name', 'task', 'layer'),
    )
    op.create_index(op.f('ix_qa_gate_thresholds_thresholds_id'), 'qa_gate_thresholds', ['thresholds_id'],
                    unique=False)

    # What qa_gate cited per task was the first layer: keep it as layer 0.
    for task, column in _FIRST_LAYER:
        op.execute(
            f"INSERT INTO qa_gate_thresholds (processing_id, pfs_visit_id, camera_name, task, layer, thresholds_id)"
            f" SELECT processing_id, pfs_visit_id, camera_name, '{task}', 0, {column}"
            f" FROM qa_gate WHERE {column} IS NOT NULL"
        )
    for _, column in _FIRST_LAYER:
        op.drop_column('qa_gate', column)

    op.alter_column('qa_thresholds', 'name', existing_type=sa.String(),
                    comment='file name, e.g. iqQaThresholds-run25.yaml; <task>.config for a config layer',
                    existing_comment='file name, e.g. iqQaThresholds-run25.yaml')


def downgrade() -> None:
    op.alter_column('qa_thresholds', 'name', existing_type=sa.String(),
                    comment='file name, e.g. iqQaThresholds-run25.yaml',
                    existing_comment='file name, e.g. iqQaThresholds-run25.yaml; <task>.config for a config layer')
    for task, column in _FIRST_LAYER:
        op.add_column('qa_gate', sa.Column(column, sa.Integer(), nullable=True))
        op.create_foreign_key(op.f(f'fk_qa_gate_{column}_qa_thresholds'), 'qa_gate', 'qa_thresholds',
                              [column], ['thresholds_id'])
        op.execute(
            f"UPDATE qa_gate g SET {column} = t.thresholds_id FROM qa_gate_thresholds t"
            f" WHERE t.processing_id = g.processing_id AND t.pfs_visit_id = g.pfs_visit_id"
            f" AND t.camera_name = g.camera_name AND t.task = '{task}' AND t.layer = 0"
        )
    op.drop_index(op.f('ix_qa_gate_thresholds_thresholds_id'), table_name='qa_gate_thresholds')
    op.drop_table('qa_gate_thresholds')
