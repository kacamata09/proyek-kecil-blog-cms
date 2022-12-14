"""empty message

Revision ID: dd4742dd8de7
Revises: d8be3230d1ab
Create Date: 2022-09-19 21:26:04.541272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd4742dd8de7'
down_revision = 'd8be3230d1ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flasklogin-pengguna', sa.Column('password_hash', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flasklogin-pengguna', 'password_hash')
    # ### end Alembic commands ###
