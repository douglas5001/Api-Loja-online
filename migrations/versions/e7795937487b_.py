"""empty message

Revision ID: e7795937487b
Revises: 8e1df4eed300
Create Date: 2024-05-11 21:43:39.015408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7795937487b'
down_revision = '8e1df4eed300'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('produto', sa.Column('imagem', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('produto', 'imagem')
    # ### end Alembic commands ###
