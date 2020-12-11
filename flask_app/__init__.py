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
from werkzeug.utils import secure_filename
from .client import SpotifyClient
# from users import users
# from movies import movies 
# stdlib
from datetime import datetime
import os



db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
client = SpotifyClient(client_id, client_secret)

# Blueprints