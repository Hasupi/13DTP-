from flask import Flask, render_template
import sqlite3
from prisma import prisma

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html', title="Home")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.errorhandler(404)
def die(e):
    return render_template("404.html", title="Error"), 404

if __name__ == "__main__":
    app.run(debug="true", host="0.0.0.0", port="8000")
