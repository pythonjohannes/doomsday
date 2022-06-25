from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///stats.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class AllYears(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(250), unique=False, nullable=False)
    time = db.Column(db.String, nullable=False)
    time_per_date = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)

class ThisYear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(250), unique=False, nullable=False)
    time = db.Column(db.String, nullable=False)
    time_per_date = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)

class OnlyYears(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(250), unique=False, nullable=False)
    time = db.Column(db.String, nullable=False)
    time_per_date = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)


db.create_all()