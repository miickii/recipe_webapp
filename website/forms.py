from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField, TextAreaField, HiddenField, SelectField
from wtforms.validators import ValidationError, DataRequired
from website.models import Ingredient

class RecipeForm(FlaskForm):
    recipe_id = HiddenField()
    name = StringField('Name', validators=[DataRequired()])
    image = StringField('Image Link')
    description = TextAreaField('Description')
    categories = SelectField('Category', choices=[], validators=[DataRequired()])
    ingredients = StringField('Ingredients')
    ingredients_amt = StringField('Ingredients')
    servings = SelectField('Servings', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16')])
    prep_time = SelectField('Prep Time', choices=[('0', '0'), ('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55'), ('60', '60')])
    cook_time = SelectField('Cook Time', choices=[('0', '0'), ('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55'), ('60', '60')])
    theme_color = StringField('Theme Color')
    notes = TextAreaField('Notes')
    hidden_categories = HiddenField()
    hidden_ingredients = HiddenField()
    hidden_steps = HiddenField()
    submit_add_recipe = SubmitField('Add Recipe')

class AddIngredientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ingredient_type = StringField('Type')
    submit_add_ingredient = SubmitField('Submit')

    '''
    def validate_name(self, name):
        name = Ingredient.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError("Ingredient already exists")'''

class UpdateIngredientForm(FlaskForm):
    ingredient_id = HiddenField()
    name = StringField('Name', validators=[DataRequired()])
    ingredient_type = StringField('Type')
    submit_update_ingredient = SubmitField('Submit')

class AddCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    color = StringField('Theme Color')
    submit_add_category = SubmitField('Submit')

class UpdateCategoryForm(FlaskForm):
    category_id = HiddenField()
    name = StringField('Name', validators=[DataRequired()])
    color = StringField('Theme Color')
    submit_update_category = SubmitField('Submit')