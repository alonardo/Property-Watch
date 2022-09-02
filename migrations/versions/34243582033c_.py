"""empty message

Revision ID: 34243582033c
Revises: 2239f73d2b54
Create Date: 2022-09-01 21:48:35.399563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34243582033c'
down_revision = '2239f73d2b54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_poke')
    op.drop_table('pokemon')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('pokemon_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ability', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('base_experience', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('attack_base_stat', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hp_base_stat', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('defense_stat', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='pokemon_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('user_poke',
    sa.Column('pokemon_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], name='user_poke_pokemon_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_poke_user_id_fkey')
    )
    # ### end Alembic commands ###