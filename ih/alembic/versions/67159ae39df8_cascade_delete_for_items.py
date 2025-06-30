"""cascade delete for items

Revision ID: 67159ae39df8
Revises: a0db01543d72
Create Date: 2025-06-27 11:42:26.420782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '67159ae39df8'
down_revision: Union[str, None] = 'a0db01543d72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_category_name', table_name='category')
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=False)

    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'item_household_id_fkey',
            'household',
            ['household_id'],
            ['id'],
            ondelete='CASCADE'
        )

    with op.batch_alter_table('itemcategorylink', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'itemcategorylink_item_id_fkey',
            'item',
            ['item_id'],
            ['id'],
            ondelete='CASCADE'
        )
        batch_op.create_foreign_key(
            'itemcategorylink_category_id_fkey',
            'category',
            ['category_id'],
            ['id'],
            ondelete='CASCADE'
        )


def downgrade() -> None:
    with op.batch_alter_table('itemcategorylink', schema=None) as batch_op:
        batch_op.drop_constraint('itemcategorylink_item_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('itemcategorylink_category_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'itemcategorylink_item_id_fkey',
            'item',
            ['item_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'itemcategorylink_category_id_fkey',
            'category',
            ['category_id'],
            ['id']
        )

    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_constraint('item_household_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'item_household_id_fkey',
            'household',
            ['household_id'],
            ['id']
        )

    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.create_index('ix_category_name', 'category', ['name'], unique=True)
