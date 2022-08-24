"""create posts table

Revision ID: bbebcbddfba4
Revises: 
Create Date: 2022-08-24 15:30:33.873432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbebcbddfba4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts', 
            sa.Column('idx', sa.Integer, nullable=False, primary_key=True),
            sa.Column('title', sa.String, nullable=False),
            sa.Column('content', sa.String(), nullable=False),
            sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.func.now())
        )


def downgrade() -> None:
    op.drop_table('posts')
