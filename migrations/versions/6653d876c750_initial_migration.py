"""Initial migration.

Revision ID: 6653d876c750
Revises: 
Create Date: 2020-12-22 12:26:20.575058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6653d876c750'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manufacturer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('head_quarter', sa.String(length=20), nullable=True),
    sa.Column('founder', sa.String(length=50), nullable=True),
    sa.Column('established_year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('manufacturer_id', sa.Integer(), nullable=False),
    sa.Column('launched_year', sa.Integer(), nullable=True),
    sa.Column('top_speed', sa.Integer(), nullable=True),
    sa.Column('engine_type', sa.String(length=30), nullable=False),
    sa.Column('max_horse_power', sa.Integer(), nullable=True),
    sa.Column('zero_to_hundred', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car')
    op.drop_table('manufacturer')
    # ### end Alembic commands ###
