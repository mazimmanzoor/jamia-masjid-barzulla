from flask import Flask, render_template, request, redirect, session
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

USERNAME = "Nimaz@4321"
PASSWORD = "1234"

def load_times():
    with open("times.json", "r") as f:
        return json.load(f)

def save_times(data):
    with open("times.json", "w") as f:
        json.dump(data, f)

@app.route("/")
def index():
    times = load_times()
    today = datetime.now().strftime("%d-%m-%Y")
    return render_template("index.html", times=times, today=today)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["admin"] = True
            return redirect("/admin")
    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":
        data = {
            "fajr": request.form["fajr"],
            "zuhar": request.form["zuhar"],
            "asr": request.form["asr"],
            "magrib": request.form["magrib"],
            "isha": request.form["isha"],
            "jumah": request.form["jumah"],
            "sehri": request.form["sehri"],
            "iftar": request.form["iftar"],
             "hadith": request.form["hadith"] 
        }
        save_times(data)
        return redirect("/")

    times = load_times()
    return render_template("admin.html", times=times)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/cron-update")
def cron_update():
    return "Cron Success", 200
if __name__ == "__main__":
    app.run()




