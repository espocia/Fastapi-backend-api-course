"""add foreign key to posts table

Revision ID: 223c042b2a4e
Revises: 6b6948a80d5e
Create Date: 2024-09-13 01:18:13.161983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '223c042b2a4e'
down_revision: Union[str, None] = '6b6948a80d5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                          source_table="posts",
                          referent_table="users",
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
