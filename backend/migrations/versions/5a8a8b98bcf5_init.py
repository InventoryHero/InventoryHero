"""init

Revision ID: 5a8a8b98bcf5
Revises: 
Create Date: 2024-03-10 19:44:36.612840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a8a8b98bcf5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=1024), nullable=False),
    sa.Column('email_confirmed', sa.Boolean(), nullable=False),
    sa.Column('confirmation_code', sa.Uuid(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('first_name', sa.String(length=80), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('confirmation_code'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('household',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=65535), nullable=False),
    sa.Column('creator', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creator'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('token_blacklist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('token_blacklist', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_token_blacklist_jti'), ['jti'], unique=False)

    op.create_table('household_members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('household_id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('invite', sa.Uuid(), nullable=True),
    sa.Column('joined', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['household_id'], ['household.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=65535), nullable=False),
    sa.Column('household_id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['household_id'], ['household.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=65535), nullable=False),
    sa.Column('household_id', sa.Integer(), nullable=False),
    sa.Column('starred', sa.Boolean(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['household_id'], ['household.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('box',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=65535), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('household_id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['household_id'], ['household.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_container_mapping',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('storage_id', sa.Integer(), nullable=True),
    sa.Column('storage_type', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_container_mapping')
    op.drop_table('box')
    op.drop_table('products')
    op.drop_table('location')
    op.drop_table('household_members')
    with op.batch_alter_table('token_blacklist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_blacklist_jti'))

    op.drop_table('token_blacklist')
    op.drop_table('household')
    op.drop_table('user')
    # ### end Alembic commands ###