"""add default now to tags.created_at

Revision ID: 54e78adbd8e8
Revises: b3a2b520c2f3
Create Date: 2026-02-21 13:17:38.363004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54e78adbd8e8'
down_revision: Union[str, Sequence[str], None] = 'b3a2b520c2f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "tags",
        "created_at",
        server_default=sa.text("now()"),
        existing_type=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "tags",
        "created_at",
        server_default=None,
        existing_type=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )
