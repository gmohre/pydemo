import urllib.request
import urllib.parse
import json

from flask import Blueprint, request, jsonify
from flask import current_app as app
from werkzeug.exceptions import NotFound
from .models import Hero, db
from .util import marvel_hash

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/query', methods=('POST',))
def query():
    hero_name = request.form.get('hero_name')
    if not hero_name:
        error = "Hero name required"
        return jsonify({'error':error})
    try:
        hero = Hero.query.\
            filter(Hero.name.ilike(f"%{hero_name}%")).first_or_404()
    except NotFound as e:
        ts, m_hash, api_key = marvel_hash()
        hero_name = urllib.parse.quote(hero_name)
        query_url = f"{app.config.get('MARVEL_BASE_URL')}/v1/public/characters?ts={ts}&name={hero_name}&hash={m_hash}&apikey={api_key}"
        print(query_url)    
        with urllib.request.urlopen(query_url) as response:
            res = response.read()
        data = json.loads(res.decode('utf-8')).get('data', {})
        results = data.get('results', [])
        if any(results):   
            hero_res = results[0]
            thumbnail = '.'.join(hero_res['thumbnail'].values())
            hero = Hero(name=hero_res['name'], thumbnail_url=thumbnail, marvel_id=hero_res['id'])
            db.session.add(hero)
            db.session.commit()
        else:
            error = "No Hero"
            return jsonify({'error':error})
    return jsonify(hero.serialize())
