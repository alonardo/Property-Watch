"""empty message

Revision ID: 2239f73d2b54
Revises: 580a10be23fb
Create Date: 2022-09-01 13:27:12.734076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2239f73d2b54'
down_revision = '580a10be23fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('agent_phone', sa.String(), nullable=True))
    op.drop_column('user', 'icon')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('icon', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('property', 'agent_phone')
    # ### end Alembic commands ###
