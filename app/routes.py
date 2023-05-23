import sys
from flask import render_template, request, redirect, url_for, session, flash, make_response
from app import app, db
from app.models import Event
from app.forms import EventForm
from app import models


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    form = EventForm()
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
    return render_template("school_task.html")


@app.route("/personal", methods=["GET", "POST"])
def personal_task():
    return render_template("personal_task.html")


@app.route("/today", methods=["GET", "POST"])
def today():
    return render_template("today.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")
