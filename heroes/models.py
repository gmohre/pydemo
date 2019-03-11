from flask import current_app as app
import json
import urllib
from heroes import db
from werkzeug.exceptions import NotFound

from .util import marvel_hash

team_heroes = db.Table('team_heroes', db.metadata,
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('hero_id', db.Integer, db.ForeignKey('heroes.id'), primary_key=True)
)

class MarvelQuery(db.Model):
    __tablename__ = 'marvelqueries'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    querystring = db.Column(db.String)
    api = db.Column(db.String())

    def _get_marvel_data(self, api, qs):
        ts, m_hash, api_key = marvel_hash()
        if not all((ts, m_hash, api_key)):
            raise NotFound('Query Data Missing')
        print(api)
        print(qs)
        query_value = urllib.parse.quote(qs)
        query_url = f"{app.config.get('MARVEL_BASE_URL')}/v1/public/{api}?ts={ts}&{qs}&hash={m_hash}&apikey={api_key}"
        print(query_url)
        with urllib.request.urlopen(query_url) as response:
            res = response.read()
        data = json.loads(res.decode('utf-8')).get('data', {})
        results = data.get('results', [])
        if any(results):
            hero_res = results[0]
            print(len(results))
            thumbnail = '.'.join(hero_res['thumbnail'].values())
            return dict(name=hero_res['name'], thumbnail_url=thumbnail, marvel_id=hero_res['id'])
        else:
            raise NotFound('hero')


    def __init__(self, querystring, api):
        self.api = api
        self.querystring = querystring
        marvel_data = self._get_marvel_data(api, querystring)
        hero = Hero(marvel_data['name'], marvel_data['thumbnail_url'], marvel_data['marvel_id'])
        db.session.add(hero)
        db.session.commit()
        self.hero_id = hero.id
    
    def serialize(self):
        return {
            'querystring' : self.querystring,
            'api' : self.api,
            'hero' : self.hero.serialize()
        }

class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    marvel_id = db.Column(db.Integer)
    name = db.Column(db.String)
    thumbnail_url = db.Column(db.String())
    queries = db.relationship('MarvelQuery', backref='hero', lazy=True)


    def __init__(self, name, thumbnail_url, marvel_id):
        self.name = name
        self.thumbnail_url = thumbnail_url
        self.marvel_id = marvel_id

    def __repr__(self):
        return f"<id {self.id}"
    
    def serialize(self):
        return {
            'id': self.id,
            'marvel_id': self.marvel_id,
            'name': self.name,
            'thumbnail_url': self.thumbnail_url
        }

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    heroes = db.relationship(Hero, secondary=team_heroes, backref=db.backref('teams'))
    
    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'heroes': [hero for hero in self.heroes]
        }