from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length

class SearchForm(FlaskForm):
    search_query = StringField('Search', validators=[InputRequired(), Length(min=1, max=30)])
    input_type = SelectField('Type', choices=['Track', 'Artist', 'Album'], validators=[InputRequired()])
    submit = SubmitField('Submit')