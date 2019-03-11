import urllib.request
import urllib.parse
import json

from flask import Blueprint, request, jsonify
from flask import current_app as app
from werkzeug.exceptions import NotFound
from .models import Hero, MarvelQuery, db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/heroes', methods=['GET'])
def heroes():
    heroes = Hero.query.all() or []
    return jsonify([hero.serialize() for hero in heroes])

@bp.route('/query', methods=('POST',))
def query():
    d = json.dumps(request.json)
    d = request.json
    hero_name = d.get('hero_name')
    if not hero_name:
        error = "Hero name required"
        return jsonify({'error':error})
    try:
        qs = f"name={hero_name}"
        prev_query = MarvelQuery.query.filter_by(querystring=qs, api='characters').first_or_404()
        return jsonify(prev_query.serialize())
    except NotFound as e:
        query_res = MarvelQuery(querystring=qs, api='characters')
        db.session.add(query_res)
        db.session.commit()
        return jsonify(query_res.serialize())