from flask import render_template, request, redirect, url_for, session, flash
from app import app

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/calendar", methods=["GET", "POST"])
def login():
    return render_template("calendar.html")

@app.route("/school-tasks", methods=["GET", "POST"])
def school_task():
    return render_template("school_task.html")

@app.route("/personal-tasks", methods=["GET", "POST"])
def personal_task():
    return render_template("personal_task.html")

@app.route("/today", methods=["GET", "POST"])
def today():
    return render_template("today.html")

@app.route("profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")