from app import db

# add event table with columns id, name, description, date, colour
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(144), nullable=False)
    date = db.Column(db.Date, nullable=False)
    colour = db.Column(db.String(144), nullable=False)
