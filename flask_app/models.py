from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
import base64
import pyotp



@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    otp_secret = db.StringField(required=True, min_length=16, max_length=16, default=pyotp.random_base32())

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    music_id = db.StringField(required=True)
    input_type = db.StringField(required=True)
    song_title = db.StringField(required=True, min_length=1, max_length=100)

class Song(db.Document):
    user = db.ReferenceField(User, required=True)
    song = db.StringField(required=True, unique=True)
    artist = db.StringField(required=True)
    album = db.StringField(required=True)