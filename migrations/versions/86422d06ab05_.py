"""empty message

Revision ID: 86422d06ab05
Revises: be82abf8513d
Create Date: 2024-06-29 18:11:46.465016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86422d06ab05'
down_revision = 'be82abf8513d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('profile_pic')

    # ### end Alembic commands ###
