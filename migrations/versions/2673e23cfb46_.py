"""empty message

Revision ID: 2673e23cfb46
Revises: 
Create Date: 2021-05-02 15:49:34.360470

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2673e23cfb46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('line', sa.String(length=20), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('schedule_time', sa.DateTime(), nullable=True),
    sa.Column('result', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('calls')
    # ### end Alembic commands ###
