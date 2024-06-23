from main import db, login_manager
from flask_login import UserMixin
from wtforms import TextAreaField
from flask_admin.contrib.sqla import ModelView
import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    nickname = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True, nullable=False)
    rank = db.Column(db.String(50), nullable=False, default='წევრი')
    score = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    in_group = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    group = db.relationship('Group', back_populates='members')

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    leader_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250))
    category = db.Column(db.String(100), nullable=False)
    members = db.relationship('User', back_populates='group')
    score = db.Column(db.Integer, nullable=False, default=0)

    @property
    def members_list(self):
        return json.loads(self.members) if self.members else []
    
    @members_list.setter
    def members_list(self, members):
        self.members = json.dumps(members)



class discountElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(120), nullable=False)
    expiration_duration = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(2500), nullable=False)
    categories = db.Column(db.String(200), nullable=False)
    img = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Discount(name: '{self.name}', condition: {self.condition}, img: {self.img})"
    
class eventElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2500), nullable=False)
    categories = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    event_hoster = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    img = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f"Event(name: '{self.name}', img: {self.img})"


class email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)

    def __repr__(self):
        return f"email - {self.email}"
    