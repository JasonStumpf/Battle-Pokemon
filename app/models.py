from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

catching = db.Table(
    'caught',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    number_of_wins = db.Column(db.Integer, default=0)
    number_of_loses = db.Column(db.Integer, default=0)

    catching = db.relationship('Pokemon',
        secondary = 'caught',
        backref = 'catching',
        lazy = 'dynamic'
    )

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.number_of_wins = 0
        self.number_of_loses = 0

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def catch(self, pokemon):
        self.catching.append(pokemon)
        db.session.commit()

    def release(self, pokemon):
        self.catching.remove(pokemon)
        db.session.commit()

    def count_wins(self):
        self.number_of_wins += 1
        db.session.commit()

    def count_loses(self):
        self.number_of_loses -= 1
        db.session.commit()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ability = db.Column(db.String, nullable=False)
    sprite = db.Column(db.String, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    caught_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)
    
    def __init__(self, name, ability, sprite, hp, attack, defense):
        self.name = name
        self.ability = ability
        self.sprite = sprite
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def save_poke(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'ability' : self.ability,
            'sprite' : self.sprite,
            'hp' : self.hp,
            'attack' : self.attack,
            'defense' : self.defense
        }