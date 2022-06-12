from flask import Flask
from config import Config
from .extensions import db, migrate # The dot . means at the same level as this file

# If i want to play with the database in python interpreter with the create_app() pattern i have to do:
'''
from myapp import create_app, db
app = create_app()
app.app_context().push()
db.create_all()
'''

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    from website.errors import errors
    app.register_blueprint(errors)

    from .main import views
    app.register_blueprint(views)

    from website import models

    return app

