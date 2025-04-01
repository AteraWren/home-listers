from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    class Meta:
        csrf = False  # Disable CSRF protection

    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[DataRequired()])