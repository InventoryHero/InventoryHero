"""empty message

Revision ID: 87f7cdf81436
Revises: 01ff6198f7ea
Create Date: 2024-09-04 23:01:28.521620

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '87f7cdf81436'
down_revision = '01ff6198f7ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('box')
    op.drop_table('location')
    with op.batch_alter_table('product_container_mapping', schema=None) as batch_op:
        batch_op.drop_column('storage_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_container_mapping', schema=None) as batch_op:
        batch_op.add_column(sa.Column('storage_type', sa.INTEGER(), autoincrement=False, nullable=False))

    op.create_table('location',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('location_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=65535), autoincrement=False, nullable=False),
    sa.Column('household_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('creation_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('type', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['household_id'], ['household.id'], name='location_household_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='location_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('box',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=65535), autoincrement=False, nullable=False),
    sa.Column('location_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('household_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('creation_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('type', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['household_id'], ['household.id'], name='box_household_id_fkey'),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], name='box_location_id_fkey', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name='box_pkey')
    )
    # ### end Alembic commands ###