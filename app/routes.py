from sqlalchemy import inspect
from flask import render_template, request, redirect, url_for, session
from flask import flash, jsonify
from app import app, db
from app.models import Event, Task, User
from app.forms import EventForm, TaskForm, TodayForm, Login, CreateAccount
from app import models
from datetime import date, timedelta
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash

# login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Get the id of the current user"""
    # since the user_id is just the primary key of our user table,
    # use it in the query for the user
    return User.query.get(int(user_id))


def object_as_dict(obj):
    """Convert a sqlalchemy object containing a date object to a dictionary -
    this is for the calendar display"""
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs if c.key != "date"
            } | {"date": str(getattr(obj, "date"))}


@app.route("/data.json")
def serve_js():
    """Send the events data to the Javascript file"""
    events = Event.query.filter_by(user_id=current_user.id).all()
    return jsonify([object_as_dict(event) for event in events])


@app.errorhandler(404)
def page_not_found(e):
    """If the entered url doesn't exist, return this page"""
    return render_template('404.html'), 404


@app.route("/", methods=["GET", "POST"])
def home():
    """Home page - login and create account from here"""
    session['colour'] = "#357DED"
    colour = session['colour']
    login_form = Login()
    acc_form = CreateAccount()
    remember = True if request.form.get('remember') else False
    if request.method == "POST":
        action = request.form["login"]
        if action == "login":
            user = User.query.filter_by(
                username=login_form.username.data).first()
            password = login_form.password.data
            # check if input password equals the hashed password
            # in the database
            if user and check_password_hash(user.password, password):
                login_user(user, remember=remember)
                flash("Logged in successfully :)", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Incorrect username or password :(", "error")
        else:
            # checking if the email or username
            # is already being used by another user
            if acc_form.email.data in [
               user.email for user in User.query.all()]:
                flash(
                    "Email already taken, please use another one", "error")
            elif acc_form.username.data in [
                 user.username for user in User.query.all()]:
                flash(
                    "Username already taken, please use another one", "error")
            else:
                new_user = models.User()
                new_user.username = acc_form.username.data
                new_user.password = generate_password_hash(
                    acc_form.password.data, method="sha256")
                new_user.email = acc_form.email.data
                db.session().add(new_user)
                db.session().commit()
                flash("Account created :)", "success")
    return render_template(
        "home.html", login_form=login_form, acc_form=acc_form, colour=colour)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    # events to be displayed
    events = Event.query.filter_by(user_id=current_user.id).order_by(
        Event.date).all()
    upcoming = []
    for event in events:
        if len(upcoming) < 3:
            upcoming.append(event)
    # tasks to be displayed
    school_tasks = Task.query.filter_by(today=True).filter_by(
        user_id=current_user.id).filter_by(type=1).order_by(Task.date).all()
    personal_tasks = Task.query.filter_by(today=True).filter_by(
        user_id=current_user.id).filter_by(type=2).order_by(Task.date).all()
    # display user streak
    streak = current_user.streak
    return render_template("dashboard.html", upcoming=upcoming,
                           school_tasks=school_tasks,
                           personal_tasks=personal_tasks, streak=streak)


@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    """Display the calendar and add events to the calendar"""
    form = EventForm()
    # choices for the dropdown menu
    form.colour.choices = [("#ff0000", "Red"), ("#357ded", "Blue"), (
        "#5f8575", "Green"), ("#ff5f1f", "Orange"), (
            "#7852a9", "Purple")]
    events = Event.query.filter_by(user_id=current_user.id).order_by(
        Event.date).all()
    upcoming = []
    for event in events:
        if len(upcoming) < 3:
            upcoming.append(event)
    if request.method == "POST":
        action = request.form["action"]
        # adding a new event
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
            flash("Event added :)", "success")
            return redirect(url_for("calendar"))
        # editing an existing event
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
            flash("Event edited :)", "success")
            return redirect(url_for("calendar"))
        # deleting an event
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            event = Event.query.get(id)
            db.session.delete(event)
            db.session().commit()
            flash("Event deleted :)", "success")
            return redirect(url_for("calendar"))
    return render_template(
        "calendar.html", form=form, events=events, upcoming=upcoming)


@app.route("/calendar/<string:formattedDate>", methods=["GET", "POST"])
@login_required
def event(formattedDate):
    form = EventForm()
    # choices for the dropdown menu
    form.colour.choices = [("#ff0000", "Red"), ("357ded", "Blue"), (
        "#5f8575", "Green"), ("#ff5f1f", "Orange"), ("#7852a9", "Purple")]
    # events = Event.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        action = request.form["action"]
        # adding a new event
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
            flash("Event added :)", "success")
            return redirect(url_for("calendar"))
        # editing an existing event
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
            flash("Event edited :)", "success")
            return redirect(url_for("calendar"))
        # deleting an event
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            event = Event.query.get(id)
            db.session.delete(event)
            db.session().commit()
            flash("Event deleted :)", "success")
            return redirect(url_for("calendar"))

    events = Event.query.filter_by(date=formattedDate).filter_by(
        user_id=current_user.id).all()
    return render_template(
        "days.html", formattedDate=formattedDate, form=form, events=events)


@app.route("/school", methods=["GET", "POST"])
@login_required
def school_task():
    """Display the school tasks and add tasks to the list"""
    form = TaskForm()
    # choices for the dropdown menu
    form.type.choices = [(1, "School"), (2, "Personal")]
    form.event.choices = [(event.id, event.name) for event in Event.query.
                          filter_by(user_id=current_user.id).all()]
    form.event.choices.append((0, "Other"))
    # filter the tasks based on their date
    # urgent tasks are due within 3 days of the current date
    urgent = Task.query.filter_by(type="1").filter(
        Task.date <= date.today() + timedelta(days=3)).filter_by(
        user_id=current_user.id).order_by(Task.date).all()
    # coming up tasks are due within 3-7 days of the current date
    coming_up = Task.query.filter_by(type="1").filter(
        date.today() + timedelta(days=3) < Task.date).filter_by(
        user_id=current_user.id).filter(
            Task.date <= date.today() + timedelta(days=7)).order_by(
                Task.date).all()
    # not urgent tasks are due more than 7 days from the current date
    not_urgent = Task.query.filter_by(type="1").filter(
        date.today() + timedelta(days=7) < Task.date).filter_by(
        user_id=current_user.id).order_by(Task.date).all()
    if request.method == "POST":
        action = request.form["action"]
        # adding a new task
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
            flash("Task added :)", "success")
            return redirect(url_for("school_task"))
        # editing an existing task
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
            flash("Task edited :)", "success")
            return redirect(url_for("school_task"))
        # deleting a task
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            task = Task.query.get(id)
            db.session.delete(task)
            db.session().commit()
            flash("Task deleted :)", "success")
            return redirect(url_for("school_task"))
    return render_template("school_task.html", form=form, urgent=urgent,
                           coming_up=coming_up, not_urgent=not_urgent)


@app.route("/personal", methods=["GET", "POST"])
@login_required
def personal_task():
    """Display the personal tasks and add tasks to the list"""
    form = TaskForm()
    # choices for the dropdown menu
    form.type.choices = [(1, "School"), (2, "Personal")]
    form.event.choices = [(event.id, event.name) for event in Event.query.
                          filter_by(user_id=current_user.id).all()]
    form.event.choices.append((0, "Other"))
    # filter Tasks by events that have a date
    # within 3 days of the current date and by the user logged in
    urgent = Task.query.filter_by(type="2").filter(
        Task.date <= date.today() + timedelta(days=3)).filter_by(
            user_id=current_user.id).order_by(Task.date).all()
    coming_up = Task.query.filter_by(type="2").filter(
        date.today() + timedelta(days=3) < Task.date).filter(
            Task.date <= date.today() + timedelta(days=7)).filter_by(
                user_id=current_user.id).order_by(Task.date).all()
    not_urgent = Task.query.filter_by(type="2").filter(
        date.today() + timedelta(days=7) < Task.date).filter_by(
            user_id=current_user.id).order_by(Task.date).all()
    if request.method == "POST":
        action = request.form["action"]
        # adding a new task
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
            flash("Task added :)", "success")
            return redirect(url_for("personal_task"))
        # editing an existing task
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
            flash("Task edited :)", "success")
            return redirect(url_for("personal_task"))
        # deleting a task
        elif action == "delete":
            print("delete")
            id = request.form["id"]
            task = Task.query.get(id)
            db.session.delete(task)
            db.session().commit()
            flash("Task deleted :)", "success")
            return redirect(url_for("personal_task"))
    return render_template("personal_task.html", urgent=urgent,
                           coming_up=coming_up, not_urgent=not_urgent,
                           form=form)


@app.route("/today", methods=["GET", "POST"])
@login_required
def today():
    """Set and display the tasks to be completed today.
    Also display progress and streak"""
    form = TodayForm()
    streak = current_user.streak
    total = current_user.total
    completed_tasks = len(Task.query.filter_by(completed=True).filter_by(
        user_id=current_user.id).all())
    if request.method == "POST":
        action = request.form["action"]
        # selecting hours
        if action == "select":
            print("select")
            # streak tracker
            # checking if all tasks for today have been completed
            completed = Task.query.filter_by(completed=True).filter_by(
                user_id=current_user.id).all()
            print(len(completed))
            print(total)
            if len(completed) != 0 and len(completed) == total:
                current_user.streak += 1
                streak = current_user.streak
                db.session().commit()
            else:
                # reset streak to 0 if
                # the user didn't complete all tasks for today
                current_user.streak = 0
                streak = current_user.streak
                db.session().commit()
            # deleting the completed tasks
            for task in Task.query.filter_by(completed=True).filter_by(
                 user_id=current_user.id).all():
                db.session().delete(task)
                db.session().commit()
            completed = []
            school_time = 0
            personal_time = 0
            school_hours = form.school.data
            personal_hours = form.personal.data
            # found a bug where if the user didn't input a value for the hours,
            # it would be NoneType
            if school_hours is None:
                school_hours = 0
            if personal_hours is None:
                personal_hours = 0
            if len(Task.query.filter_by(user_id=current_user.id).all()) == 0:
                flash("Please add some tasks to do", "error")
            else:
                for task in Task.query.order_by(Task.date).filter_by(
                 user_id=current_user.id).all():
                    # reset all tasks to False i.e. not today's task
                    task.today = False
                    db.session().commit()
                    # adding task to the today list as long as the total hours
                    # doesn't exceed the value input by the user
                    if task.type == "1":
                        if school_time + task.hours <= school_hours:
                            school_time += task.hours
                            task.today = True
                            db.session().commit()
                    else:
                        if personal_time + task.hours <= personal_hours:
                            personal_time += task.hours
                            task.today = True
                            db.session().commit()
                total = len(Task.query.filter_by(today=True).filter_by(
                    user_id=current_user.id).all())
                current_user.total = total
                db.session().commit()
            return redirect(url_for("today"))
        # when user is checking off completed tasks
        elif action == "done":
            tasks_done = request.form.getlist("task")
            for id in tasks_done:
                task = Task.query.filter_by(id=id).one()
                task.today = False
                task.completed = True
                db.session().commit()
                completed_tasks = len(Task.query.filter_by(
                    completed=True).filter_by(user_id=current_user.id).all())
        else:
            # if the user checked off a task by accident,
            #  they can undo it by unchecking the box
            undo = request.form.getlist("task_done")
            for task_id in Task.query.with_entities(Task.id).filter_by(
                 completed=True).filter_by(user_id=current_user.id).all():
                # task_id is a tuple
                if str(task_id[0]) not in undo:
                    task = Task.query.filter_by(id=task_id[0]).one()
                    task.today = True
                    task.completed = False
                    db.session().commit()
            completed_tasks = len(Task.query.filter_by(
                completed=True).filter_by(user_id=current_user.id).all())
    school_tasks = Task.query.filter_by(today=True).filter_by(
        user_id=current_user.id).filter_by(type=1).order_by(Task.date).all()
    personal_tasks = Task.query.filter_by(today=True).filter_by(
        user_id=current_user.id).filter_by(type=2).order_by(Task.date).all()
    completed = Task.query.filter_by(completed=True).filter_by(
        user_id=current_user.id).all()
    return render_template("today.html", form=form, school_tasks=school_tasks,
                           personal_tasks=personal_tasks, completed=completed,
                           streak=streak, total=total,
                           completed_tasks=completed_tasks)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Display the user's profile and change their password,
    username, email and background colour"""
    # retrieving the user's background colour from the database
    colour = current_user.colour
    session['colour'] = colour
    username_original = current_user.username
    email_original = current_user.email
    if request.method == "POST":
        action = request.form['action']
        # changing password
        if action == "password":
            print("password")
            password = request.form["password"]
            password2 = request.form["password2"]
            # checking if the input password and confirm password match
            if password == password2:
                user = User.query.get(current_user.id)
                # hash new password
                user.password = generate_password_hash(
                    password, method="scrypt")
                db.session().commit()
                flash("Password changed :)", "success")
            else:
                flash("Passwords don't match :(", "error")
            redirect(url_for("profile"))
        # changing username
        elif action == "username":
            print("username")
            username = request.form["username"]
            # checking if username is already being used by another user
            if username in [user.username for user in User.query.all()]:
                flash(
                    "Username already taken, please use another one", "error")
                username = username_original
            else:
                user = User.query.get(current_user.id)
                user.username = username
                db.session().commit()
                flash("Username changed :)", "success")
            redirect(url_for("profile"))
        # changing email
        elif action == "email":
            print("email")
            email = request.form["email"]
            # checking if username is already being used by another user
            if email in [user.email for user in User.query.all()]:
                flash("Email already taken, please use another one", "error")
            else:
                user = User.query.get(current_user.id)
                user.email = email
                db.session().commit()
                flash("Email changed :)", "success")
            redirect(url_for("profile"))
    return render_template("profile.html", username_original=username_original,
                           email_original=email_original)


@app.route("/logout")
@login_required
def logout():
    """Logout the user"""
    logout_user()
    flash("Logged out successfully :)", "success")
    return redirect("/")
