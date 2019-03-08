from heroes import db

team_heroes = db.Table('team_heroes', db.metadata,
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('hero_id', db.Integer, db.ForeignKey('heroes.id'), primary_key=True)
)

class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    marvel_id = db.Column(db.Integer)
    name = db.Column(db.String)
    thumbnail_url = db.Column(db.String())
    
    def __init__(self, name, thumbnail_url):
        self.name = name
        self.thumbnail_url = thumbnail_url

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