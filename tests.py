from datetime import datetime, timedelta
import unittest
from website import create_app, db
from website.models import Recipe, Ingredient, Category
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # A unit test to check if adding Recipe works
    def test_add_recipe(self):
        apple = Ingredient(name='apple', ingredient_type='fruit')
        cake = Ingredient(name='cake', ingredient_type='dessert')
        noodle = Ingredient(name='noodle', ingredient_type='pasta')
        water = Ingredient(name='water', ingredient_type='liquid')
        soy_sauce = Ingredient(name='soy sauce', ingredient_type='liquid')
        cup_noodle = Recipe(name='cup noodle', description='Delicious and easy noodles', servings=1, prep_time=2, cook_time=5, total_time=7, instructions='1. Open lid, 2. Add water, 3. Wait 5 mins, 4. Enjoy!', notes='add extra stuff')
        apple_cake = Recipe(name='apple cake', description='Delicious and easy dessert', servings=6, prep_time=20, cook_time=30, total_time=50, instructions='1. Make dough, 2. Cut apples, 3. Mix apples with cream, 4. Form dough and add apple mix!, 5. Put in oven, 6. Wait 30 mins, 7. Enjoy!', notes='good with vanilla cream')
        db.session.add(apple)
        db.session.add(cake)
        db.session.add(noodle)
        db.session.add(water)
        db.session.add(soy_sauce)
        db.session.add(cup_noodle)
        db.session.add(apple_cake)
        db.session.commit()

        self.assertEqual(cup_noodle.ingredients.all(), [])
        self.assertEqual(apple_cake.ingredients.all(), [])

        cup_noodle.add_ingredients([noodle])
        cup_noodle.add_ingredients([water, soy_sauce])
        db.session.commit()

        self.assertTrue(cup_noodle.has_ingredient(water))
        self.assertEqual(cup_noodle.ingredients.count(), 3)
        self.assertEqual(cup_noodle.ingredients.first().name, 'noodle')

        cup_noodle.remove_ingredients([soy_sauce])
        db.session.commit()

        self.assertFalse(cup_noodle.has_ingredient(soy_sauce))
        self.assertEqual(cup_noodle.ingredients.count(), 2)

        toast_with_butter = Recipe(name='toast with butter', description='Delicious and easy toast', servings=1, prep_time=4, cook_time=2, total_time=6, instructions='1. Put toast in toaster, 2. Wait 5 mins, 3. Spread butter, 4. Enjoy!', notes='add peanutbutter')
        butter = Ingredient(name='butter', ingredient_type='dairy')
        toast = Ingredient(name='toast', ingredient_type='bread')
        easy = Category(name='easy')
        bread = Category(name='bread')
        good = Category(name='good')
        db.session.add(butter)
        db.session.add(toast)
        db.session.add(toast_with_butter)
        db.session.add(easy)
        db.session.add(bread)
        db.session.add(good)
        db.session.commit()

        toast_with_butter.add_ingredients([toast, butter])
        toast_with_butter.add_categories([easy, bread])
        db.session.commit()

        self.assertTrue(toast_with_butter.has_ingredient(butter))
        self.assertEqual(toast_with_butter.ingredients.count(), 2)
        self.assertEqual(toast_with_butter.categories.count(), 2)

        toast_with_butter.remove_categories([bread, easy])
        toast_with_butter.add_categories([good])
        db.session.commit()
        self.assertEqual(toast_with_butter.categories.first().name, 'good')


if __name__ == '__main__':
    unittest.main(verbosity=2)
