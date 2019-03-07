import urllib.request
import urllib.parse
import time
import hashlib
import json
from flask import Blueprint, request, jsonify
from flask import current_app as app
from .models import Hero, db
from .util import marvel_hash
bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/query', methods=('POST',))
def query():
    hero_name = request.form.get('hero_name')
    if not hero_name:
        error = "Hero name required"
    else:
        hero = Hero.query.\
            filter(Hero.name.ilike(f"%{hero_name}%")).first()
    if not hero:
        ts, m_hash, api_key = marvel_hash()        
        hero_name = urllib.parse.quote(hero_name)
        query_url = f"https://gateway.marvel.com/v1/public/characters?ts={ts}&name={hero_name}&hash={m_hash}&apikey={api_key}"
        print(query_url)
        
        with urllib.request.urlopen(query_url) as response:
            res = response.read()
        
        data = json.loads(res.decode('utf-8')).get('data', {})
        results = data.get('results', [])
        hero = results[0]
        thumbnail = '.'.join(hero['thumbnail'].values())
        hero = Hero(name=hero['name'], thumbnail_url=thumbnail)
        db.session.add(hero)
        db.session.commit()
    if hero:
        return jsonify(hero.serialize())
    return jsonify({})
