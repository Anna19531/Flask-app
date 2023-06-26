from sqlalchemy import inspect
from flask import render_template, request, redirect, url_for, session, flash, make_response, jsonify
from app import app, db
from app.models import Event, Task, User
from app.forms import EventForm, TaskForm, TodayForm, Login, CreateAccount
from app import models
from datetime import date, timedelta
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

#login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

    
#convert a sqlalchemy object containing a date object to a dictionary
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs if c.key != "date"} | {"date": str(getattr(obj, "date"))}

@app.route("/data.json")
def serve_js():
    events = Event.query.all()
    return jsonify([object_as_dict(event) for event in events])


@app.route("/", methods = ["GET", "POST"])
def home():
    login_form = Login()
    acc_form = CreateAccount()
    remember = True if request.form.get('remember') else False
    if request.method == "POST":
        action = request.form["login"]
        if action == "login":
            user = User.query.filter_by(username = login_form.username.data).first()
            password = login_form.password.data
            #check if input password equals the hashed password in the database
            if user and check_password_hash(user.password, password):
                login_user(user, remember = remember)
                flash("Logged in successfully :)")
                return redirect(url_for("today"))
            else:
                flash("Incorrect username or password :(")
        else:
            new_user = models.User()
            new_user.username = acc_form.username.data
            new_user.password = generate_password_hash(acc_form.password.data, method = "sha256")
            new_user.email = acc_form.email.data
            db.session().add(new_user)
            db.session().commit()
            flash("Account created :)")
    return render_template("home.html", login_form=login_form, acc_form=acc_form)


@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    form = EventForm()
    #choices for the dropdown menu
    form.colour.choices = [(1, "Red"), (2, "Blue"), (3, "Green"), (4, "Yellow"), (5, "Orange"), (6, "Purple"), (7, "Black")]
    events = Event.query.filter_by(user_id = current_user.id).all()
    if request.method  == "POST":
        action = request.form["action"]
        if action == "add":
            print("add")
            new_event = models.Event()
            new_event.name = form.name.data
            new_event.description = form.description.data
            new_event.date = form.date.data
            new_event.colour = form.colour.data
            new_event.user_id = current_user.id
            db.session().add(new_event)
            db.session().commit()
            flash("Event added :)")
            return redirect(url_for("calendar"))
        elif action == "edit":
            print("edit")
            id = request.form["id"]
            event = Event.query.get(id)
            event.name = form.name.data
            event.description = form.description.data
            event.date = form.date.data
            event.colour = form.colour.data
            event.user_id = current_user.id
            db.session().commit()
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            event = Event.query.get(id)
            db.session.delete(event)
            db.session().commit()
            return redirect(url_for("calendar"))
    return render_template("calendar.html", form=form, events=events)


@app.route("/school", methods=["GET", "POST"])
@login_required
def school_task():
    form = TaskForm()
    #choices for the dropdown menu
    form.type.choices = [(1, "School"), (2, "Personal")]
    form.event.choices = [(event.id, event.name) for event in Event.query.filter_by(user_id = current_user.id).all()]
    urgent = Task.query.filter_by(type = "1").filter(Task.date <= date.today() + timedelta(days=3)).filter_by(user_id = current_user.id).order_by(Task.date).all()
    coming_up = Task.query.filter_by(type = "1").filter(date.today() + timedelta(days=3) < Task.date).filter_by(user_id = current_user.id).filter(Task.date <= date.today() + timedelta(days=7)).order_by(Task.date).all()
    not_urgent = Task.query.filter_by(type = "1").filter(date.today() + timedelta(days=7) < Task.date).filter_by(user_id = current_user.id).order_by(Task.date).all()
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
            new_task.hours = form.hours.data
            new_task.user_id = current_user.id
            db.session().add(new_task)
            db.session().commit()
            flash("Task added :)")
            return redirect(url_for("school_task"))
        elif action == "edit":
            print("edit")
            id = request.form["id"]
            task = Task.query.get(id)
            task.name = form.name.data
            task.description = form.description.data
            task.date = form.date.data
            task.type = form.type.data
            task.event_id = form.event.data
            task.hours = form.hours.data
            task.user_id = current_user.id
            db.session().commit()
            flash("Task edited :)")
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            task = Task.query.get(id)
            db.session.delete(task)
            db.session().commit()
            flash("Task deleted :)")
            return redirect(url_for("school_task"))
    return render_template("school_task.html", form=form, urgent=urgent, coming_up=coming_up, not_urgent=not_urgent)


@app.route("/personal", methods=["GET", "POST"])
@login_required
def personal_task():
    form = TaskForm()
    #choices for the dropdown menu
    form.type.choices = [(1, "School"), (2, "Personal")]
    form.event.choices = [(event.id, event.name) for event in Event.query.filter_by(user_id = current_user.id).all()]
    #filter Tasks by events that have a date within 3 days of the current date and by the user logged in
    urgent = Task.query.filter_by(type = "2").filter(Task.date <= date.today() + timedelta(days=3)).filter_by(user_id = current_user.id).order_by(Task.date).all()
    coming_up = Task.query.filter_by(type = "2").filter(date.today() + timedelta(days=3) < Task.date).filter(Task.date <= date.today() + timedelta(days=7)).filter_by(user_id = current_user.id).order_by(Task.date).all()
    not_urgent = Task.query.filter_by(type = "2").filter(date.today() + timedelta(days=7) < Task.date).filter_by(user_id = current_user.id).order_by(Task.date).all()
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
            new_task.hours = form.hours.data
            new_task.user_id = current_user.id
            db.session().add(new_task)
            db.session().commit()
            flash("Task added :)")
            return redirect(url_for("personal_task"))
        elif action == "edit":
            print("edit")
            id = request.form["id"]
            task = Task.query.get(id)
            task.name = form.name.data
            task.description = form.description.data
            task.date = form.date.data
            task.type = form.type.data
            task.event_id = form.event.data
            task.hours = form.hours.data
            task.user_id = current_user.id
            db.session().commit()
            flash("Task edited :)")
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            task = Task.query.get(id)
            db.session.delete(task)
            db.session().commit()
            flash("Task deleted :)")
            return redirect(url_for("personal_task"))
    return render_template("personal_task.html", urgent=urgent, coming_up=coming_up, not_urgent=not_urgent, form=form)


@app.route("/today", methods=["GET", "POST"])
@login_required
def today():
    form = TodayForm()
    school_time = 0
    personal_time = 0
    school_tasks = []
    personal_tasks = []
    if request.method == "POST":
        school_hours = form.school.data
        personal_hours = form.personal.data
        print(school_hours)
        for task in Task.query.order_by(Task.date).all():
            if task.type == "1":
                if school_time + task.hours <= school_hours:
                    school_time += task.hours
                    school_tasks.append(task)
            else:
                if personal_time + task.hours <= personal_hours:
                    personal_time += task.hours
                    personal_tasks.append(task)
    return render_template("today.html", form=form, school_tasks=school_tasks, personal_tasks=personal_tasks)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out succesfully :)")
    return redirect("/")
