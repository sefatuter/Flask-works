"""Added Post Model

Revision ID: 8a5193dd08b9
Revises: 44d0a05bcf36
Create Date: 2024-06-23 19:43:39.869518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a5193dd08b9'
down_revision = '44d0a05bcf36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('context', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('author', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('date_posted', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('slug', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('slug')
        batch_op.drop_column('date_posted')
        batch_op.drop_column('author')
        batch_op.drop_column('context')
        batch_op.drop_column('title')

    # ### end Alembic commands ###
