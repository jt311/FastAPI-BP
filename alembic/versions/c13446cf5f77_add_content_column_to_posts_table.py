"""Add content column to Posts table

Revision ID: c13446cf5f77
Revises: 7b0fc8cccd09
Create Date: 2023-01-23 10:28:34.727392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c13446cf5f77'
down_revision = '7b0fc8cccd09'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String, nullable = False))


def downgrade() -> None:
    op.drop_column("posts", "content")
