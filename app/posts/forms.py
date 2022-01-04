from flask_wtf import FlaskForm
# from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired(), Length(min=2, max=50)])
    content = TextAreaField('Content', validators = [DataRequired()])
    submit = SubmitField('Submit')