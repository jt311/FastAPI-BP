"""Create Posts Table

Revision ID: 7b0fc8cccd09
Revises: 
Create Date: 2023-01-23 10:17:48.083859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b0fc8cccd09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",
    sa.Column('id', sa.Integer, nullable = False, primary_key = True),
    sa.Column('title', sa.String, nullable = False))

def downgrade() -> None:
    op.drop_table("posts")
