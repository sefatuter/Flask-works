"""about author added

Revision ID: eaacfb18ebe8
Revises: cac67267ae00
Create Date: 2024-06-29 17:40:32.693811

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eaacfb18ebe8'
down_revision = 'cac67267ae00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('author')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_author', sa.Text(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('about_author')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', mysql.VARCHAR(length=255), nullable=True))

    # ### end Alembic commands ###