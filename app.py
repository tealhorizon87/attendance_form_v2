import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
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
                "guest_1_name": request.form.get("guest_1_name"),
                "guest_1_dining": request.form.get("guest_1_dining"),
                "guest_1_diet": request.form.get("guest_1_diet"),
                "guest_1_sponsor": request.form.get("name"),
            }
            mongo.db.guest_data.insert_one(guest1)
        if guest_2_name:
            guest2 = {
                "guest_2_name": request.form.get("guest_2_name"),
                "guest_2_dining": request.form.get("guest_2_dining"),
                "guest_2_diet": request.form.get("guest_2_diet"),
                "guest_2_sponsor": request.form.get("name"),
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
        return render_template("admin.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():

    return render_template("admin.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
