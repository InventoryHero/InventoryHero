"""password reset token timezone awarae

Revision ID: a4178de77f42
Revises: bd2d7adde6b1
Create Date: 2025-07-22 08:32:12.300337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a4178de77f42'
down_revision: Union[str, None] = 'bd2d7adde6b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to make datetime timezone-aware."""
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column(
            "password_reset_token_expires_at",
            existing_type=sa.DateTime(timezone=False),
            type_=sa.DateTime(timezone=True),
            existing_nullable=True
        )


def downgrade() -> None:
    """Downgrade schema to make datetime timezone-naive."""
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column(
            "password_reset_token_expires_at",
            existing_type=sa.DateTime(timezone=True),
            type_=sa.DateTime(timezone=False),
            existing_nullable=True
        )
