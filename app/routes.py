import sys
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect
from flask import render_template, request, redirect, url_for, session, flash, make_response, jsonify
from app import app, db
from app.models import Event, Task
from app.forms import EventForm, TaskForm
from app import models

    
#convert a sqlalchemy object containing a date object to a dictionary
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs if c.key != "date"} | {"date": str(getattr(obj, "date"))}

@app.route("/data.json")
def serve_js():
    events = Event.query.all()
    return jsonify([object_as_dict(event) for event in events])


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    form = EventForm()
    #choices for the dropdown menu
    form.colour.choices = [(1, "Red"), (2, "Blue"), (3, "Green"), (4, "Yellow"), (5, "Orange"), (6, "Purple"), (7, "Black")]
    events = Event.query.all()
    if request.method  == "POST":
        action = request.form["action"]
        if action == "add":
            print("add")
            new_event = models.Event()
            new_event.name = form.name.data
            new_event.description = form.description.data
            new_event.date = form.date.data
            new_event.colour = form.colour.data
            db.session().add(new_event)
            db.session().commit()
            msg = "OK" if new_event else sys.last_value
            return make_response(msg, 200)
        elif action == "edit":
            print("edit")
            id = request.form["id"]
            event = Event.query.get(id)
            event.name = form.name.data
            event.description = form.description.data
            event.date = form.date.data
            event.colour = form.colour.data
            db.session().commit()
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            event = Event.query.get(id)
            db.session.delete(event)
            db.session().commit()
    return render_template("calendar.html", form=form, events=events)


@app.route("/school", methods=["GET", "POST"])
def school_task():
    form = TaskForm()
    #choices for the dropdown menu
    form.type.choices = [(1, "School"), (2, "Personal")]
    form.event.choices = [(event.id, event.name) for event in Event.query.all()]
    tasks = Task.query.all()
    if request.method  == "POST":
        action = request.form["action"]
        if action == "add":
            print("add")
            new_task = models.Task()
            new_task.name = form.name.data
            new_task.description = form.description.data
            new_task.date = form.date.data
            new_task.type = form.type.data
            new_task.event_id = form.event.data
            db.session().add(new_task)
            db.session().commit()
            msg = "OK" if new_task else sys.last_value
            return make_response(msg, 200)
        elif action == "edit":
            print("edit")
            id = request.form["id"]
            task = Task.query.get(id)
            task.name = form.name.data
            task.description = form.description.data
            task.date = form.date.data
            task.type = form.type.data
            task.event_id = form.event.data
            db.session().commit()
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            task = Task.query.get(id)
            db.session.delete(task)
            db.session().commit()
    return render_template("school_task.html", form=form, tasks=tasks)


@app.route("/personal", methods=["GET", "POST"])
def personal_task():
    form = TaskForm()
    #choices for the dropdown menu
    form.type.choices = [(1, "School"), (2, "Personal")]
    form.event.choices = [(event.id, event.name) for event in Event.query.all()]
    tasks = Task.query.all()
    if request.method  == "POST":
        action = request.form["action"]
        if action == "add":
            print("add")
            new_task = models.Task()
            new_task.name = form.name.data
            new_task.description = form.description.data
            new_task.date = form.date.data
            new_task.type = form.type.data
            new_task.event_id = form.event.data
            db.session().add(new_task)
            db.session().commit()
            msg = "OK" if new_task else sys.last_value
            return make_response(msg, 200)
        elif action == "edit":
            print("edit")
            id = request.form["id"]
            task = Task.query.get(id)
            task.name = form.name.data
            task.description = form.description.data
            task.date = form.date.data
            task.type = form.type.data
            task.event_id = form.event.data
            db.session().commit()
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            task = Task.query.get(id)
            db.session.delete(task)
            db.session().commit()
    return render_template("personal_task.html", tasks=tasks, form=form)


@app.route("/today", methods=["GET", "POST"])
def today():
    return render_template("today.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")
