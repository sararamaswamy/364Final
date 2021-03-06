"""fourth

Revision ID: 4b7d560f91eb
Revises: 6c7390a2334b
Create Date: 2017-12-10 18:27:13.144637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b7d560f91eb'
down_revision = '6c7390a2334b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actors', sa.Column('movie_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'actors', 'movies', ['movie_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'actors', type_='foreignkey')
    op.drop_column('actors', 'movie_id')
    # ### end Alembic commands ###
