from flask import Flask, render_template, redirect, url_for
import sqlite3
from prisma import Prisma, register
from __init__ import app, login_manager
from user import UserClass
from flask_login import login_user, logout_user, login_required
from prisma.models import User

@login_manager.user_loader
def user_loader(user_id):
    user = User.prisma().find_first(where={
        'id' : int(user_id)
    })
    return UserClass(user.__dict__)


@app.route("/")
def home():
    return render_template('home.html', title="Home")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/login")
def login():
    user_data = User.prisma().find_first(
        where={
            'name' : 'Shane'
        }
    )
    print(user_data)
    user = UserClass(user_data.__dict__)
    login_user(user)
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.errorhandler(404)
def die(e):
    return render_template("404.html", title="Error"), 404

if __name__ == "__main__":
    app.run(debug="true", host="0.0.0.0", port="8000")
