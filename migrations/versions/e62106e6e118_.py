"""empty message

Revision ID: e62106e6e118
Revises: 3fe6b8444d34
Create Date: 2020-06-14 23:04:44.313011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e62106e6e118'
down_revision = '3fe6b8444d34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'booked_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('booked_date', sa.DATETIME(), nullable=False))
    # ### end Alembic commands ###
