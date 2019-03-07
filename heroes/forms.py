from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class HeroQueryForm(FlaskForm):
    hero_name = StringField('hero_name', validators=[DataRequired()])