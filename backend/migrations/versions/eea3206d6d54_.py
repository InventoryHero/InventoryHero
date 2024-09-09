"""empty message

Revision ID: eea3206d6d54
Revises: 8beaed04c1fb
Create Date: 2024-07-14 19:46:33.534993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eea3206d6d54'
down_revision = '8beaed04c1fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('password_reset_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('password_reset_hash', sa.String(length=1024), nullable=False),
    sa.Column('password_reset_time', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('password_reset_requests')
    # ### end Alembic commands ###
