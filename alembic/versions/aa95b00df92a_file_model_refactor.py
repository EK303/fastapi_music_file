"""File model refactor

Revision ID: aa95b00df92a
Revises: 37ae3bff312a
Create Date: 2023-05-24 18:37:54.262228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa95b00df92a'
down_revision = '37ae3bff312a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('audiofile_uploader_slug_key', 'audiofile', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('audiofile_uploader_slug_key', 'audiofile', ['uploader_slug'])
    # ### end Alembic commands ###
