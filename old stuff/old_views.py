# OLD FORM URLS
@views.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    if request.method == 'POST':
        name = request.form['name']
        i_type = request.form['food_type']

        ingredient = Ingredient(name=name, ingredient_type=i_type)
        db.session.add(ingredient)
        db.session.commit()

        flash("Ingredient Added")

        return redirect(url_for('views.ingredients'))

@views.route('/add_category', methods=['POST'])
def add_category():

    '''if request.method == 'POST':
        name = request.form['name']

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()

        flash("Category Added")

        return redirect(url_for('views.ingredients'))'''

@views.route('/update-ingredient', methods=['GET', 'POST'])
def update_ingredient():
    if request.method == 'POST':
        ingredient = Ingredient.query.get(request.form['id'])
        ingredient.name = request.form['name']
        ingredient.ingredient_type = request.form['type']
        db.session.commit()

        flash('Ingredient Updated!')
        return redirect(url_for('views.ingredients'))

@views.route('/update-category', methods=['GET', 'POST'])
def update_category():
    if request.method == 'POST':
        category = Category.query.get(request.form['id'])
        category.name = request.form['name']
        db.session.commit()

        flash('Category Updated!')
        return redirect(url_for('views.ingredients'))