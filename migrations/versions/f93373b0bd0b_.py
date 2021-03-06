"""empty message

Revision ID: f93373b0bd0b
Revises: cffa80fc35bd
Create Date: 2022-05-29 00:18:28.122781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f93373b0bd0b'
down_revision = 'cffa80fc35bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('steps', sa.String(length=4294000000), nullable=True))
    op.drop_column('recipe', 'instructions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('instructions', sa.VARCHAR(length=4294000000), nullable=True))
    op.drop_column('recipe', 'steps')
    # ### end Alembic commands ###
