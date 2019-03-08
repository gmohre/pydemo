from flask import request, render_template, Blueprint, jsonify
from flask import current_app as app
from .models import db, Hero, Team
from .forms import HeroQueryForm
bp = Blueprint('heroes', __name__, url_prefix='/heroes')

@bp.route('/', methods=['GET'])
def heroes():
    heroes = Hero.query.all() or []
    return jsonify([hero.serialize() for hero in heroes])

@bp.route('/find', methods=['GET, POST'])
def find():
    form = HeroQueryForm()
    return render_template('hero_query_form.html', form=form)