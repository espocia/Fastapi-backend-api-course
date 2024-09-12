"""add remaining posts columns

Revision ID: 7c13ede30549
Revises: 223c042b2a4e
Create Date: 2024-09-13 01:24:02.101312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c13ede30549'
down_revision: Union[str, None] = '223c042b2a4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('create_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))

def downgrade() -> None:
    op.drop_column('posts', 'published' )
    op.drop_column('posts', 'create_at' )
