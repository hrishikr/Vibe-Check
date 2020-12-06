from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Length
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

#from flask_app.models import User  # we still need to define models.py

class SearchForm(FlaskForm):
    search_query = StringField('Search', validators=[InputRequired(), Length(min=1, max=30)])
    input_type = SelectField('Type', choices=['Track', 'Artist', 'Album'], validators=[InputRequired()])
    submit = SubmitField('Submit')

# Registration Form that we will be using to render our Registration page. Has all required information.
class RegistrationForm(FlaskForm):    
    email = StringField("Email", validators = [InputRequired(), Email()])
    username = StringField("Username", validators = [InputRequired(), Length(min = 1, max = 60)])
    password = PasswordField("Password", validators = [InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [InputRequired(), EqualTo(password)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.objects(username = username.data).first()
        if user is not None:
            raise ValidationError("Username has already been taken")
    
    def validate_email(self, email):
        user = User.objects(email = email.data).first()
        if user is not None:
            raise ValidationError("Email is already taken")

# Login Form that we will be using to render our Login page. Has all required information.
class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    submit = SubmitField("Login")

# Update Username Form in the case that any of the registered and logged in users need to change their usernames.
class UpdateUsernameForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username = username.data).first()
            if user is not None:
                raise ValidationError("This username is already taken")


