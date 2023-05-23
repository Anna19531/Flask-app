from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SelectField, validators, StringField, DateField
from wtforms.validators import Optional, ValidationError, DataRequired

# form to add events
class EventForm(FlaskForm):
    name = StringField("Event name", [validators.Length(min=2, max=144)])
    description = StringField("Description", [validators.Length(min=2, max=500)])
    date = DateField("Date")
    colour = SelectField("Colour", [validators.Length(min=2, max=144)])

def eventForm(request):
    form = EventForm(request.POST)
    form.colour.choices = [(1, "Red"), (2, "Blue"), (3, "Green"), (4, "Yellow"), (5, "Orange"), (6, "Purple"), (7, "Black")]



