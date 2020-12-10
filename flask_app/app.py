#3rd-party packages
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo

# stdlib
import json
import os
from datetime import datetime

# local
from flask_app.forms import SearchForm, LoginForm, RegistrationForm
from flask_app.client import SpotifyClient

from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)

from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from .models import User

from . import bcrypt



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/my_database"
app.config['SECRET_KEY'] = b'\n\xb5\x8a\x96\xaa.+2~\xc3\x0e(?\xb0\x17\xd9'

client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
client = SpotifyClient(client_id, client_secret)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

mongo = PyMongo(app)


""" ************ View functions ************ """

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        query = {
            "search_query": form.search_query.data,
            "input_type": form.input_type.data
        }
        return redirect(url_for('query_results', query=form.search_query.data, input_type=form.input_type.data))

    return render_template('index.html', form=form)

@app.route('/search-results/<query>?<input_type>', methods=['GET'])
def query_results(query, input_type):
    try:
        results = client.get_search_results(query=query, search_type=input_type)
        return render_template('query_results.html', results=results, input_type=input_type)
    except ValueError as err:
        return render_template('query_results.html', error_msg=err)


""" ************ User Management views ************ """


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        return redirect(url_for("main.login"))

    return render_template("register.html", title="Register", form=form)