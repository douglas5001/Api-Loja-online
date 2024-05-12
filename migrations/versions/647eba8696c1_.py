"""empty message

Revision ID: 647eba8696c1
Revises: 87f1640694a1
Create Date: 2024-05-12 03:06:44.460568

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '647eba8696c1'
down_revision = '87f1640694a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('usuario_produto', 'quantidade_produto',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('usuario_produto', 'quantidade_produto',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # ### end Alembic commands ###