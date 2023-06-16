from flask_wtf import FlaskForm
from app.models import Event
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

#form to add tasks
class TaskForm(FlaskForm):
    name = StringField("Task name", [validators.Length(min=2, max=144)])
    description = StringField("Description", [validators.Length(min=2, max=500)])
    date = DateField("Date")
    type = SelectField("Type", [validators.Length(min=2, max=144)])
    event = SelectField("Event", [validators.Length(min=2, max=144)])
    #need to change hours so that you can only select integer values
    hours = IntegerField("Hours", [validators.NumberRange(min=0, max=24)])
    #category = SelectField("Category", [validators.Length(min=2, max=144)])

def taskForm(request):
    form = TaskForm(request.POST)
    form.type.choices = [(1, "School"), (2, "Personal")]
    form.event.choices = [(event.id, event.name) for event in Event.query.all()]

#form to decide how much time to spend on school and personal tasks
class TodayForm(FlaskForm):
    school = IntegerField("School", [validators.NumberRange(min=0, max=24)])
    personal = IntegerField("Personal", [validators.NumberRange(min=0, max=24)])




