from flask import Flask, render_template, redirect, url_for, request
from __init__ import app, login_manager, db
from user import User
from flask_login import login_user, logout_user, login_required
from wtforms import StringField, validators, PasswordField, SubmitField
from prisma import models
from flask_wtf import FlaskForm


app.config["SECRET_KEY"] = 'totally_secret_key'


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=6, max=99)])
    email = StringField('Email Address', [validators.Length(min=12, max=35)])
    password = PasswordField('Password', [validators.Length(min=8, max=99)])
    submit = SubmitField('Submit')


@login_manager.user_loader
def user_loader(user_id):
    user = User.prisma().find_first(where={
        'id': int(user_id)
    })
    if not user:
        return None
    else:
        return User(user.__dict__)


@app.route("/")
def home():
    user = db.user.find_many()
    print(user)
    return render_template('home.html', title="Home", user=user)


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/login", methods=['GET', 'POST'])
def login():
    class LoginForm(FlaskForm):
        username = StringField('Username')
        password = PasswordField('Password')
        submit = SubmitField("Submit")
    form = LoginForm()

    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        # return redirect('/')
        login_user(User)

        Flask.flash('Logged in successfully.')

        next = Flask.request.args.get('next')
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # See Django's url_has_allowed_host_and_scheme for an example.
        if not url_has_allowed_host_and_scheme(next, request.host):
            return Flask.abort(400)

        return redirect(next or Flask.url_for('/'))
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/signup", methods=['POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        models.User.prisma().create(
            data={
                'name': form.username.data,
                'password': form.password.data,
            }
        )
    return redirect(url_for('signup'))


@app.route("/register")
def signup():
    form = RegistrationForm()
    return render_template("signup.html", form=form)


@app.errorhandler(404)
def die(e):
    return render_template("404.html", title="Error"), 404


if __name__ == "__main__":
    app.run(debug="true", host="0.0.0.0", port="8000")
