"""Initial migration

Revision ID: 9bf602214f97
Revises: 
Create Date: 2025-09-23 07:08:23.890217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bf602214f97'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'words',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('word', sa.String(length=100), nullable=False),
        sa.Column('input_times', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('meaning', sa.Text(), nullable=False),
        sa.Column('create_time', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('update_time', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('word'),
    )

    op.create_table(
        'study_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('word_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('create_time', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('update_time', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['word_id'], ['words.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index('ix_study_records_word_id', 'study_records', ['word_id'])


def downgrade():
    op.drop_index('ix_study_records_word_id', table_name='study_records')
    op.drop_table('study_records')
    op.drop_table('words')
