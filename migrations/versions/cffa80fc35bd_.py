"""empty message

Revision ID: cffa80fc35bd
Revises: dacd2e43760d
Create Date: 2022-05-26 15:56:39.639366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cffa80fc35bd'
down_revision = 'dacd2e43760d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('img', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'img')
    # ### end Alembic commands ###
