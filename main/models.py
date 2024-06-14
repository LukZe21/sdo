from main import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

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

    # @property
    # def formatted_duration(self):
    #     """Returns the duration in hours and minutes."""
    #     if self.duration:
    #         return f"{self.end_date-self.start_date} hr"
    #     return None
    
    def __repr__(self):
        return f"Event(name: '{self.name}', img: {self.img})"


class email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)

    def __repr__(self):
        return f"email - {self.email}"
