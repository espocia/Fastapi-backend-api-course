"""add: create content column

Revision ID: aca96e0b5b86
Revises: f33280564833
Create Date: 2024-09-13 01:03:03.874671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aca96e0b5b86'
down_revision: Union[str, None] = 'f33280564833'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
