# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object("config")

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

migrate = Migrate(app, db)
# Import a module / component using its blueprint handler variable (mod_auth)
from app.manfacturer_car_module.views import manufacturer_car_module

# Register blueprint(s)
app.register_blueprint(manufacturer_car_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
