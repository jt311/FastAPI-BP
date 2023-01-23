"""Create User Table

Revision ID: a4711252d866
Revises: c13446cf5f77
Create Date: 2023-01-23 10:39:21.741773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4711252d866'
down_revision = 'c13446cf5f77'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer, nullable = False, primary_key = True),
                    sa.Column('email', sa.String, unique = True, nullable = False),
                    sa.Column('password', sa.String, nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default = sa.text('now()')))


def downgrade() -> None:
    op.drop_table('users')
