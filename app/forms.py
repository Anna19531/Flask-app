from flask_wtf import FlaskForm
from app.models import Event
from wtforms import IntegerField, SelectField, validators, StringField, DateField, EmailField, PasswordField
from wtforms.validators import Optional, ValidationError, DataRequired

# form to add events
class EventForm(FlaskForm):
    name = StringField("Event name", validators = [validators.Length(min=1, max=144), validators.DataRequired()])
    description = StringField("Description", [validators.Length(min=2, max=500)])
    date = DateField("Date", validators = [validators.DataRequired()])
    colour = SelectField("Colour", [validators.Length(min=1, max=144)])

def eventForm(request):
    form = EventForm(request.POST)
    form.colour.choices = [(1, "Red"), (2, "Blue"), (3, "Green"), (4, "Yellow"), (5, "Orange"), (6, "Purple"), (7, "Black")]

#form to add tasks
class TaskForm(FlaskForm):
    name = StringField("Task name", validators = [validators.Length(min=1, max=144), validators.DataRequired()])
    description = StringField("Description", [validators.Length(min=1, max=500)])
    date = DateField("Date", validators = [validators.DataRequired()])
    type = SelectField("Type", [validators.Length(min=2, max=144)])
    event = SelectField("Event", [validators.Length(min=2, max=144)])
    hours = IntegerField("Hours it will take", validators = [validators.NumberRange(min=0, max=24), validators.DataRequired()])
    #category = SelectField("Category", [validators.Length(min=2, max=144)])

def taskForm(request):
    form = TaskForm(request.POST)
    form.type.choices = [(1, "School"), (2, "Personal")]
    #need to have "other" as an option
    form.event.choices = [((event.id, event.name) for event in Event.query.all()), (0, "Other")]

#form to decide how much time to spend on school and personal tasks
class TodayForm(FlaskForm):
    school = IntegerField("School", [validators.NumberRange(min=0, max=24)])
    personal = IntegerField("Personal", [validators.NumberRange(min=0, max=24)])

class Login(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])

class CreateAccount(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    password2 = PasswordField("Password again: ", validators=[DataRequired()])
    email = EmailField("Email: ", validators=[DataRequired()])


