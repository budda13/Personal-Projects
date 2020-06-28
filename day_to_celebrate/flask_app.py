from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="thespis89",
    password="nosey711",
    hostname="thespis89.mysql.pythonanywhere-services.com",
    databasename="thespis89$celebrations",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Celebrate(db.Model):

    __tablename__ = "day_of"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    scope = db.Column(db.String(10))
    content = db.Column(db.String(200))

global_days = []
national_days = []
send = False

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("main_page.html")

    m = request.form["month"]
    d = request.form["DOBDay"]

    global_days = Celebrate.query.filter(Celebrate.month == m, Celebrate.day == d, Celebrate.scope == "Global").all()
    national_days = Celebrate.query.filter(Celebrate.month == m, Celebrate.day == d, Celebrate.scope == "National").all()

    print("Global:", file=sys.stderr)
    for i in global_days:
        print(i.content, file=sys.stderr)

    print("National:", file=sys.stderr)
    for i in national_days:
        print(i.content, file=sys.stderr)

    return render_template("main_page.html", global_days=global_days, national_days=national_days)