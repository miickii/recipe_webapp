"""empty message

Revision ID: dbf786254d1f
Revises: 
Create Date: 2022-05-18 09:45:16.749563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbf786254d1f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('ingredient_type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=1400), nullable=True),
    sa.Column('ingredients_amount', sa.String(length=4000), nullable=True),
    sa.Column('servings', sa.Integer(), nullable=True),
    sa.Column('prep_time', sa.Integer(), nullable=True),
    sa.Column('cook_time', sa.Integer(), nullable=True),
    sa.Column('total_time', sa.Integer(), nullable=True),
    sa.Column('instructions', sa.String(length=4294000000), nullable=True),
    sa.Column('notes', sa.String(length=1400), nullable=True),
    sa.Column('theme_color', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipe_name'), 'recipe', ['name'], unique=True)
    op.create_table('recipe_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipe_ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('ingredient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredient.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe_ingredient')
    op.drop_table('recipe_category')
    op.drop_index(op.f('ix_recipe_name'), table_name='recipe')
    op.drop_table('recipe')
    op.drop_table('ingredient')
    op.drop_table('category')
    # ### end Alembic commands ###
