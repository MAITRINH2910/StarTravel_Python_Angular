# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import config
# Define the WSGI application object
app = Flask(__name__)

#Configurations
app.config.from_object(config.Config)

# Define the database object which is imported
# by modules and user_api
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

bcrypt.init_app(app)
db.init_app(app)

# Import a module / component using its blueprint handler variable (mod_auth)

from app.api.user_api import user_api

from app.api.hotel_api import hotel_api

from app.api.feedback_api import feedback_api

# Register blueprint(s)
app.register_blueprint(user_api)

app.register_blueprint(hotel_api)

app.register_blueprint(feedback_api)

CORS(app)

# app.register_blueprint(admin_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()
