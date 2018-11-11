# encoding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    strava_token = db.Column(db.String(128))
    age = db.Column(db.Integer)
    weight = db.Column(db.Numeric(4, 1))
    max_hr = db.Column(db.Integer)
    rest_hr = db.Column(db.Integer)
    vo2max = db.Column(db.Numeric(4, 2))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        print(password, " ", self.password)
        #checked = self.password == password
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id


class Run(db.Model):
    __tablename__ = 'run'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    strava_id = db.Column(db.Integer)
    distance = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    elapsed_time = db.Column(db.Float)
    average_speed = db.Column(db.Float)
    average_heartrate = db.Column(db.Float)
    total_elevation_gain = db.Column(db.Float)
    runner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    runner = relationship('User', foreign_keys='Run.runner_id', backref=backref('Run', cascade="all,delete"))



class Objectives(db.Model):
    __tablename__ = 'user_objectives'
    distance = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = relationship('User', foreign_keys='Objectives.user_id', backref=backref('Objectives', cascade="all,delete"))

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance

class Challenge(db.Model):
    __tablename__ = 'challenge'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    runner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    runner = relationship('User', foreign_keys='Challenge.runner_id', backref=backref('Challenge', cascade="all,delete"))
    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))
    run = relationship('Run', foreign_keys='Challenge.run_id', backref=backref('Challenge', cascade="all,delete"))
    latest_run_id = db.Column(db.Integer)

def _delete_user(user):
    # delete cascade
    db.session.delete(user)
    db.session.commit()

def _setObjective(user, distance):
    new_objective = Objectives()
    new_objective.distance = distance
    new_objective.user = user
    db.session.add(new_objective)

