"""Create Vote Table

Revision ID: f42a5457243b
Revises: 5824d15ebfa4
Create Date: 2023-01-23 11:12:53.137033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f42a5457243b'
down_revision = '5824d15ebfa4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('votes',
    sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id', ondelete="CASCADE"), primary_key = True),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE"), primary_key = True))

def downgrade() -> None:
    op.drop_table('users')
