# This file takes care of all the extensions like database variable, migration engine and so on. 
# We then import these variables in the __init__.py dunder file, so they can be used in the app.
# The reason why we don't just create these variables in the __init__.py, is to avoid certain compication with circular imports.
# Its also just best practice to make the dunder __init__.py import everything from the app, not the other way around.
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()