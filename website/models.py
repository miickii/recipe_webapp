from website import db

recipe_ingredient = db.Table('recipe_ingredient',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
        db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')))

recipe_category = db.Table('recipe_category',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
        db.Column('category_id', db.Integer, db.ForeignKey('category.id')))

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    img = db.Column(db.String(64))
    description = db.Column(db.String(1400))
    categories = db.relationship('Category', secondary=recipe_category, backref=db.backref('recipes', lazy='dynamic'), lazy='dynamic')
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredient, backref=db.backref('recipes', lazy='dynamic'), lazy='dynamic')
    ingredients_amount = db.Column(db.String(4000))
    servings = db.Column(db.Integer)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    steps = db.Column(db.String(4294000000))
    notes = db.Column(db.String(1400))
    theme_color = db.Column(db.String(64))
    favorite = db.Column(db.Boolean, default=False)

    def has_ingredient(self, ingredient):
        return self.ingredients.filter(recipe_ingredient.c.ingredient_id == ingredient.id).count() > 0
    
    def add_ingredients(self, ingredients):
        for ingredient in ingredients:
            if not self.has_ingredient(ingredient):
                self.ingredients.append(ingredient)
    
    def remove_ingredients(self, ingredients):
        for ingredient in ingredients:
            if self.has_ingredient(ingredient):
                self.ingredients.remove(ingredient)

    def has_category(self, category):
        return self.categories.filter(recipe_category.c.category_id == category.id).count() > 0
    
    def add_categories(self, categories):
        for category in categories:
            if not self.has_category(category):
                self.categories.append(category)
    
    def remove_categories(self, categories):
        for category in categories:
            if self.has_category(category):
                self.categories.remove(category)
    
    # This method returns a sqlalchemy object as a dictionary. This is useful if i want to get database queries with ajax
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'img': self.img,
            'description': self.description,
           # This is an example how to deal with Many2Many relations
            'categories': self.serialize_categories(),
            'ingredients': self.serialize_ingredients(),
            'ingredients_amount': self.ingredients_amount,
            'servings': self.servings,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'total_time': self.total_time,
            'steps': self.steps,
            'notes': self.notes,
            'theme_color': self.theme_color,
            'favorite': self.favorite
        }
    
    def serialize_categories(self):
        return [item.serialize() for item in self.categories]
    
    def serialize_ingredients(self):
        return [item.serialize() for item in self.ingredients]
    
    def can_make_with_ingredients(self, ingredients):
        ingredients_as_list = [ingredient.name for ingredient in self.ingredients]
        print(ingredients_as_list)
        if set(ingredients_as_list) == set(ingredients):
            return True
        else:
            return False

    def __repr__(self):
        return 'Recipe {}'.format(self.name)

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    ingredient_type = db.Column(db.String(64))
    #recipes_rs = db.relationship('Recipe', secondary=recipe_ingredient, backref='ingredients')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredient_type': self.ingredient_type
        }
    def __repr__(self):
        return 'Ingredient {}'.format(self.name)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    color = db.Column(db.String(64))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }

    def __repr__(self):
        return 'Category {}'.format(self.name)
