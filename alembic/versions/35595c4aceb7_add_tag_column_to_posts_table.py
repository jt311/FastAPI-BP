"""Add Tag column to Posts Table

Revision ID: 35595c4aceb7
Revises: f42a5457243b
Create Date: 2023-01-23 20:37:06.771687

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '35595c4aceb7'
down_revision = 'f42a5457243b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('tag', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'users', ['tag'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'tag')
