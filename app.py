import os
from flask import Flask, render_template, request
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("home.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        return render_template("admin.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
