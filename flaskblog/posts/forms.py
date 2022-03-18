from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CrPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=50)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=3, max=250)])
    submit = SubmitField('Create')