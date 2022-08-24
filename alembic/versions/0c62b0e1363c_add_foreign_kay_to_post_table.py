"""add foreign kay to post table

Revision ID: 0c62b0e1363c
Revises: 108d5d37401a
Create Date: 2022-08-24 17:13:24.430387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c62b0e1363c'
down_revision = '108d5d37401a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("owner_id", sa.Integer, nullable=True))
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users", 
        local_cols="owner_id", remote_cols=["idx"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
