from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


# Initialize Flask app
app = Flask(__name__)
app.secret_key = "mysecretkey"

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.name}')"

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


# Login form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


# Signup form
class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")


# Routes
@app.route("/")
@login_required
def home():
    return render_template("home.html", name=current_user.name)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(email=form.email.data, name=form.name.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. You can now log in.")
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


# Initialize app
if __name__ == "__main__":
    db.create_all()
    app.run
