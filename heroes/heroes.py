from flask import request, render_template, Blueprint
from flask import current_app as app
from .models import db, Hero, Team
from .forms import HeroQueryForm
bp = Blueprint('heroes', __name__, url_prefix='/')

@app.route('/', methods=['GET'])
def heroes():
    heroes = Hero.query.all()
    return render_template('heroes.html', heroes=heroes, title="Show Heroes")

@app.route('/find', methods=['GET'])
def find():
    form = HeroQueryForm()
    return render_template('hero_query_form.html', form=form)