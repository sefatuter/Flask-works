"""Add content column to posts table

Revision ID: 575e0c57a6ec
Revises: 8a5193dd08b9
Create Date: 2024-06-23 20:08:20.479045

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '575e0c57a6ec'
down_revision = '8a5193dd08b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.Text(), nullable=True))
        batch_op.drop_column('context')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('context', mysql.TEXT(), nullable=True))
        batch_op.drop_column('content')

    # ### end Alembic commands ###