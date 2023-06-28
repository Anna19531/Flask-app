from app import db
from flask_login import UserMixin

# add event table with columns id, name, description, date, colour
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(144), nullable=False)
    date = db.Column(db.Date, nullable=False)
    colour = db.Column(db.String(144), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(144), nullable=False)
    date = db.Column(db.Date)
    type = db.Column(db.String(144), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    #category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    today = db.Column(db.Boolean)
    completed = db.Column(db.Boolean)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)

    def __repr__(self):
        return self.username
    
    def get_id(self):
        return str(self.id)
    
    
    


