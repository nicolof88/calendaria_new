from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .util import filters


# Create Flask app instance
app = Flask(__name__)
app.jinja_env.filters['nth'] = filters.nth

# Set configurations
app.config.from_object(Config)

# Set database to app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login
login = LoginManager(app)
login.login_view = 'login'


from app import routes, models, errors