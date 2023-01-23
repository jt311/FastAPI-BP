"""Create Foreign Key for Users and Posts Tables

Revision ID: 5824d15ebfa4
Revises: a4711252d866
Create Date: 2023-01-23 10:51:57.168981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5824d15ebfa4'
down_revision = 'a4711252d866'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default = 'True', nullable = False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')))
    op.add_column('posts', sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable = False))

def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'user_id')
