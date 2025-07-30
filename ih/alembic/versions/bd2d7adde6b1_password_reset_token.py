"""password reset token

Revision ID: bd2d7adde6b1
Revises: 56239b82635c
Create Date: 2025-07-22 08:15:53.655347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'bd2d7adde6b1'
down_revision: Union[str, None] = '56239b82635c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("password_reset_token", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("password_reset_token_expires_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("password_reset_token_expires_at")
        batch_op.drop_column("password_reset_token")