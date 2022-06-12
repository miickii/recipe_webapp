from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import json
from website import db
from website.forms import RecipeForm, AddIngredientForm, UpdateIngredientForm, AddCategoryForm, UpdateCategoryForm
from website.models import *

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/index')
def index():
    recipes = Recipe.query.all()
    ingredients = Ingredient.query.all()
    categories = Category.query.all()
    return render_template('main/index.html', title='Home', background="#eee", recipes=recipes, ingredients=ingredients, categories=categories)

@views.route('/test_index')
def test_index():
    recipes = [{"name": "Fried Rice", "categories": ["Easy", "Quick"], "image": "https://i.imgur.com/hmJP9AS.jpg"}, {"name": "Butter Chicken", "categories": ["Tasty", "Hard", "Indian"], "image": "https://i.imgur.com/aeKkH8b.jpg"}, {"name": "Golden Curry", "categories": ["Easy"], "image": "https://i.imgur.com/Qzlr39B.jpg"}]
    return render_template('main/test_index.html', title='Test', background='#eee', recipes=recipes)

@views.route('/get_recipes', methods=['POST'])
def get_recipes():
    category = request.form['category']
    selected_ingredients = request.form['ingredients']
    favorite = request.form['favorite']
    recipes = []

    if category != "":
        recipes = Category.query.filter_by(name=category).first().recipes
    elif selected_ingredients != "":
        selected_ingredients = selected_ingredients.split(",")
        print(selected_ingredients)
        all_recipes = Recipe.query.all()
        for recipe in all_recipes:
            if recipe.can_make_with_ingredients(selected_ingredients):
                recipes.append(recipe)
    else:
        recipes = Recipe.query.all()
    
    if favorite == "true":
        # If sort by favorite is selected, we want to remove all the recipes that aren't favorited
        recipes = [recipe for recipe in recipes if recipe.favorite]

    recipes_serialized = []
    for recipe in recipes:
        recipes_serialized.append(recipe.serialize())
    
    # jsonify is a flask method which in this case is better than json.dumps, since it creates a response that doesn't need to be processed in any way
    # because we use a $.post ajax request we want a response back which is returned by this jsonify method
    return jsonify(recipes_serialized)

@views.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    recipe_name = request.form['recipe']
    recipe = Recipe.query.filter_by(name=recipe_name).first_or_404()
    print(recipe.favorite)
    if recipe.favorite:
        # If favorite toggle off
        recipe.favorite = False
        db.session.commit()
        return "false"
    else:
        # If not favorite toggle on
        recipe.favorite = True
        db.session.commit()
        return "true"

@views.route('/recipe/<name>')
def recipe(name):
    recipe = Recipe.query.filter_by(name=name).first_or_404()
    amounts = recipe.ingredients_amount.split(",")
    steps = recipe.steps.split("@")

    return render_template('main/make_recipe.html', title='Make Recipe', recipe=recipe, amounts=amounts, steps=steps)

@views.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = RecipeForm()
    form.categories.choices = [(category.id, category.name) for category in Category.query.all()]
    ingredients = Ingredient.query.all()
    categories = Category.query.all()

    if form.submit_add_recipe.data and form.validate_on_submit():
        recipe_name = form.name.data
        img = form.image.data
        description = form.description.data
        category_ids = (form.hidden_categories.data).split(",")
        ingredient_names = (form.hidden_ingredients.data).split(",")
        while ("" in ingredient_names):
            ingredient_names.remove("")

        ingredients_amt = []
        for ingredient in ingredient_names:
            amt = request.form.get(ingredient + '-amt')
            print(amt + ingredient)
            if amt != '':
                ingredients_amt.append(amt)
            else:
                ingredients_amt.append('')
        
        servings = int(form.servings.data)
        prep_time = int(form.prep_time.data)
        cook_time = int(form.cook_time.data)
        total_time = prep_time + cook_time

        # Looping 50 times and checking if there is a corresponding step input. If so, then add it to the steps variable
        all_steps_found = False
        steps = []
        for i in range(1, 50):
            step = request.form.get('step-' + str(i))
            if step != None:
                steps.append(step)
            else:
                break
        
        notes = form.notes.data
        theme_color = form.theme_color.data

        # Getting the Category and Ingredient objects from their model
        category_items = [] # New array with each category database object
        ingredient_items = [] # New array with each ingredient database object
        for id in category_ids:
            category_items.append(Category.query.filter_by(id=id).first())
        
        for name in ingredient_names:
            ingredient_items.append(Ingredient.query.filter_by(name=name).first())
        
        print(category_items)
        print(ingredient_items)
        '''    
        categories = ','.join([str(cat) for cat in categories])
        ingredients = ','.join([str(ingredient) for ingredient in ingredients])'''

        # Turning all the lists into strings separated by comma
        ingredients_amt = ','.join([str(amt) for amt in ingredients_amt])
        steps = '@'.join([str(step) for step in steps])

        '''flash("{} Added!".format(name))
        flash("Description: {}".format(description))
        flash("Categories: {}".format(categories))
        flash("Ingredients: {}".format(ingredients))
        flash("Amounts: {}".format(ingredients_amt))
        flash("Servings: {}".format(servings))
        flash("Prep Time: {}".format(prep_time))
        flash("Cook Time: {}".format(cook_time))
        flash("Total Time: {}".format(total_time))
        flash(steps, 'info')
        flash("Notes: {}".format(notes))
        flash("Theme Color: {}".format(theme_color))'''

        recipe = Recipe(name=recipe_name,
                        img=img,
                        description=description,
                        ingredients_amount=ingredients_amt,
                        servings=servings,
                        prep_time=prep_time,
                        cook_time=cook_time,
                        total_time=total_time,
                        steps=steps,
                        notes=notes,
                        theme_color=theme_color)
        
        ''' DOESN'T WORK
        recipe.add_categories(category_items)
        recipe.add_ingredients(ingredient_items)
        '''
        
        recipe.categories = [category for category in category_items]
        recipe.ingredients = [ingredient for ingredient in ingredient_items]

        db.session.add(recipe)
        db.session.commit()
        flash("Recipe Added!")
        
        return redirect(url_for('views.add_recipe'))

    return render_template('main/add_recipe.html', title='Add Recipe', ingredients=ingredients, categories=categories, form=form)

@views.route('/ingredients', methods=['POST', 'GET'])
def ingredients():
    add_category_form = AddCategoryForm()
    update_category_form = UpdateCategoryForm()

    add_ingredient_form = AddIngredientForm()
    update_ingredient_form = UpdateIngredientForm()

    if add_ingredient_form.submit_add_ingredient.data and add_ingredient_form.validate_on_submit():
        ingredient = Ingredient.query.filter_by(name=add_ingredient_form.name.data).first()
        if ingredient:
            flash("Ingredient already exists", 'error')
        else:
            ingredient = Ingredient(name=add_ingredient_form.name.data, ingredient_type=add_ingredient_form.ingredient_type.data)
            db.session.add(ingredient)
            db.session.commit()

            flash("Ingredient Added")

        return redirect(url_for('views.ingredients'))
    
    if update_ingredient_form.submit_update_ingredient.data and update_ingredient_form.validate_on_submit():
        # First check if an ingredient with same name already exists
        ingredient_exists = Ingredient.query.filter_by(name=update_ingredient_form.name.data).first()
        if ingredient_exists and ingredient_exists.name != update_ingredient_form.name.data:
            flash("Ingredient with same name already exists", 'error')
        else:
            ingredient = Ingredient.query.filter_by(id=update_ingredient_form.ingredient_id.data).first()
            ingredient.name = update_ingredient_form.name.data
            ingredient.ingredient_type = update_ingredient_form.ingredient_type.data
            db.session.commit()

            flash('Ingredient Updated!')
        return redirect(url_for('views.ingredients'))

    if add_category_form.submit_add_category.data and add_category_form.validate_on_submit():
        category = Category.query.filter_by(name=add_category_form.name.data).first()
        if category:
            flash("Category already exists", 'error')
        else:
            category = Category(name=add_category_form.name.data, color=add_category_form.color.data)
            db.session.add(category)
            db.session.commit()

            flash("Category Added")
        return redirect(url_for('views.ingredients'))
    
    if update_category_form.submit_update_category.data and update_category_form.validate_on_submit():
        category_exists = Category.query.filter_by(name=update_category_form.name.data).first()
        if category_exists and category_exists.name != update_category_form.name.data:
            flash("Category with same name already exists", 'error')
        else:
            category = Category.query.filter_by(id=update_category_form.category_id.data).first()
            category.name = update_category_form.name.data
            category.color = update_category_form.color.data
            db.session.commit()

            flash('Category Updated!')
        return redirect(url_for('views.ingredients'))

    ings = Ingredient.query.all()
    categories = Category.query.all()

    return render_template('main/ingredients.html',
                            title='Ingredients',
                            ingredients=ings,
                            categories=categories,
                            add_cat_form=add_category_form,
                            update_cat_form=update_category_form,
                            add_ingredient_form=add_ingredient_form,
                            update_ingredient_form=update_ingredient_form)

@views.route('/delete-category/<id>', methods=['GET', 'POST'])
def delete_category(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    flash(f"{category.name} Removed")
    return redirect(url_for('views.ingredients'))

@views.route('/delete-ingredient/<id>', methods=['GET', 'POST'])
def delete_ingredient(id):
    ingredient = Ingredient.query.get(id)
    db.session.delete(ingredient)
    db.session.commit()
    flash(f"{ingredient.name} Removed")
    return redirect(url_for('views.ingredients'))


@views.route('/edit_recipe/<name>', methods=['GET', 'POST'])
def edit_recipe(name):
    recipe = Recipe.query.filter_by(name=name).first_or_404()
    recipe_serialized = recipe.serialize()
    title = 'Edit' + recipe.name

    form = RecipeForm()
    form.categories.choices = [(category.id, category.name) for category in Category.query.all()]

    ingredients = Ingredient.query.all()
    categories = Category.query.all()

    if form.submit_add_recipe.data and form.validate_on_submit():
        recipe_exists = Recipe.query.filter_by(name=form.name.data).first()
        if recipe_exists and form.name.data != recipe.name:
            flash("Recipe with same name already exists", 'error')
            return redirect(url_for('views.edit_recipe', name=recipe.name))
        else:
            recipe_name = form.name.data
            img = form.image.data
            description = form.description.data
            category_ids = (form.hidden_categories.data).split(",")
            ingredient_names = (form.hidden_ingredients.data).split(",")
            while ("" in ingredient_names):
                ingredient_names.remove("")

            ingredients_amt = []
            for ingredient in ingredient_names:
                amt = request.form.get(ingredient + '-amt')
                if amt != '':
                    ingredients_amt.append(amt)
                else:
                    ingredients_amt.append('')
            
            servings = int(form.servings.data)
            prep_time = int(form.prep_time.data)
            cook_time = int(form.cook_time.data)
            total_time = prep_time + cook_time

            # Looping 50 times and checking if there is a corresponding step input. If so, then add it to the steps variable
            all_steps_found = False
            steps = []
            for i in range(1, 50):
                step = request.form.get('step-' + str(i))
                if step != None:
                    steps.append(step)
                else:
                    break
            
            notes = form.notes.data
            theme_color = form.theme_color.data

            # Getting the Category and Ingredient objects from their model
            category_items = [] # New array with each category database object
            ingredient_items = [] # New array with each ingredient database object
            for id in category_ids:
                category_items.append(Category.query.filter_by(id=id).first())
            
            for name in ingredient_names:
                ingredient_items.append(Ingredient.query.filter_by(name=name).first())

            # Turning all the lists into strings separated by comma
            ingredients_amt = ','.join([str(amt) for amt in ingredients_amt])
            steps = '@'.join([str(step) for step in steps])

            # UPDATE THE DATABASE
            recipe = Recipe.query.filter_by(id=form.recipe_id.data).first()

            recipe.name = recipe_name
            recipe.img = img
            recipe.description = description
            recipe.ingredients_amount = ingredients_amt
            recipe.servings = servings
            recipe.prep_time = prep_time
            recipe.cook_time = cook_time
            recipe.total_time = total_time
            recipe.steps = steps
            recipe.notes = notes
            recipe.theme_color = theme_color
            
            recipe.categories = [] # Reset
            recipe.ingredients = [] # Reset
            # Repopulate
            recipe.add_categories(category_items)
            recipe.add_ingredients(ingredient_items)

            db.session.commit()
            flash("Recipe Updated!")
            
            return redirect(url_for('views.index'))
    
    # Populate form with current values from the recipe
    form.name.data = recipe.name
    form.image.data = recipe.img
    form.description.data = recipe.description
    form.servings.data = str(recipe.servings)
    form.prep_time.data = str(recipe.prep_time)
    form.cook_time.data = str(recipe.cook_time)
    form.theme_color.data = recipe.theme_color
    form.notes.data = recipe.notes
    return render_template('main/edit_recipe.html', title=title, recipe=recipe, recipe_serialized=recipe_serialized, ingredients=ingredients, categories=categories, form=form)