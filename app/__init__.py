from flask import Flask

from config import Config

from .auth.routes import auth

from .models import db, User

from flask_migrate import Migrate

from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)

login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.init_app(app)

migrate = Migrate(app, db)

login.init_app(app)

app.register_blueprint(auth)

from . import routes

from . import models