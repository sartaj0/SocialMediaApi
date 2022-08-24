"""add user table

Revision ID: 108d5d37401a
Revises: bbebcbddfba4
Create Date: 2022-08-24 17:09:05.473766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '108d5d37401a'
down_revision = 'bbebcbddfba4'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('users',
		sa.Column('idx', sa.Integer(), nullable=False),
		sa.Column('email', sa.String(), nullable=False),
		sa.Column('password', sa.String(), nullable=False),
		sa.Column('created_at', sa.TIMESTAMP(timezone=True),
					server_default=sa.sql.func.now(), nullable=False),
		sa.PrimaryKeyConstraint('idx'),
		sa.UniqueConstraint('email')
		)
	pass


def downgrade():
	op.drop_table('users')
	pass
