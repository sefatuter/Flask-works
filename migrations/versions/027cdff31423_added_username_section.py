"""Added username section

Revision ID: 027cdff31423
Revises: 575e0c57a6ec
Create Date: 2024-06-25 00:27:23.080988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '027cdff31423'
down_revision = '575e0c57a6ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=20), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
