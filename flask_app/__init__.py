# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

# local
from .client import SpotifyClient



db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
client = SpotifyClient(os.environ.get("SPOTIFY_CLIENT_ID"), os.environ.get("SPOTIFY_CLIENT_SECRET"))

# Blueprints
from .music.routes import music
from .users.routes import users

def page_not_found(e):
    return render_template("404.html"), 404

def app(test_config=None):
    app = Flask(__name__)
    csp = {
        'default-src': '\'self\'',
        'script-src':[
            '\'self\'',
            'https://stackpath.bootstrapcdn.com/bootstrap/',
            'https://code.jquery.com/',
            'https://cdnjs.cloudflare.com/ajax/libs/popper.js/'
        ],
        'style-src':[
            '\'self\'',
            'https://stackpath.bootstrapcdn.com/bootstrap/'
        ],
        'img-src':'*'
    }
    Talisman(app, content_security_policy=csp)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(music)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
