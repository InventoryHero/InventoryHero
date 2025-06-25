"""added household_id to category

Revision ID: a0db01543d72
Revises: ad2cc61fe1ab
Create Date: 2025-06-20 22:47:15.028528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'a0db01543d72'
down_revision: Union[str, None] = 'ad2cc61fe1ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('category') as batch_op:
        batch_op.add_column(sa.Column('household_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_category_household_id", 'household', ['household_id'], ['id']
        )

def downgrade():
    with op.batch_alter_table('category') as batch_op:
        batch_op.drop_constraint("fk_category_household_id", type_='foreignkey')
        batch_op.drop_column('household_id')