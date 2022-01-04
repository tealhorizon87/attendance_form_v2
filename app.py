import os
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        guest_1_name = request.form.get("guest_1_name")
        guest_2_name = request.form.get("guest_2_name")
        guest1 = {}
        guest2 = {}

        member = {
            "name": request.form.get("name"),
            "dining": request.form.get("dining"),
            "diet": request.form.get("diet"),
        }
        if guest_1_name:
            guest1 = {
                "guest_name": request.form.get("guest_1_name"),
                "guest_dining": request.form.get("guest_1_dining"),
                "guest_diet": request.form.get("guest_1_diet"),
                "guest_sponsor": request.form.get("name"),
            }
            mongo.db.guest_data.insert_one(guest1)
        if guest_2_name:
            guest2 = {
                "guest_name": request.form.get("guest_2_name"),
                "guest_dining": request.form.get("guest_2_dining"),
                "guest_diet": request.form.get("guest_2_diet"),
                "guest_sponsor": request.form.get("name"),
            }
            mongo.db.guest_data.insert_one(guest2)

        mongo.db.form_data.insert_one(member)

        return redirect(url_for("thanks"))


    return render_template("home.html")


@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


@app.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "POST":
        user = mongo.db.admin.find_one({"user": "admin"})
        if check_password_hash(user["password"], request.form.get("password")):
            return redirect(url_for("admin"))
        else:
            flash("Incorrect Password", "error")
            return redirect(url_for("home"))


@app.route("/admin", methods=["GET", "POST"])
def admin():

    attendees = list(mongo.db.form_data.find())
    guests = list(mongo.db.guest_data.find())
    member_number = len(attendees)
    guest_number = len(guests)
    total_member_dining = len(list(mongo.db.form_data.find({"dining": "True"})))
    total_guest_dining = len(list(mongo.db.guest_data.find({"guest_dining": "True"})))
    total_dining = total_member_dining + total_guest_dining

    return render_template("admin.html", attendees=attendees,
                           guests=guests, member_number=member_number,
                           guest_number=guest_number, total_dining=total_dining)


@app.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == "POST":
        mongo.db.form_data.remove({})
        mongo.db.guest_data.remove({})
        flash("Data successfully reset", "success")
        return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
