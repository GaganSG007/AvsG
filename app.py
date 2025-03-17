from flask import Flask, render_template, request, redirect, url_for, session
import json
import random
import os
from datetime import date

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

DATA_FILE = "data.json"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"G": {}, "A": {}}, f)


# Function to load data
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


# Function to save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Random motivational quotes
motivational_quotes = [
    "Keep pushing forward, {user}! 💪",
    "Every rep counts, {user}! Stay strong! 🔥",
    "You're doing amazing, {user}! Don't stop now! 🚀",
    "Sweat today, shine tomorrow, {user}! 🌟",
    "No pain, no gain, {user}! Keep grinding! 💯"
]


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        birth_year = request.form.get("otp").strip()

        if birth_year == "2001":
            session["user"] = "G"
            return redirect(url_for("home"))
        elif birth_year == "2002":
            session["user"] = "A"
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid code! Try again.")

    return render_template("login.html", error=None)


@app.route("/home", methods=["GET", "POST"])
def home():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))

    data = load_data()
    today = str(date.today())  # Gets today's date

    if request.method == "POST":
        workout_info = request.form["workout"]
        if user not in data:
            data[user] = {}
        data[user][today] = workout_info
        save_data(data)

        # Show random motivational message
        message = random.choice(motivational_quotes).format(user=user)
        return render_template("home.html", user=user, message=message, today_workout=workout_info)

    today_workout = data.get(user, {}).get(today, "No workout logged yet.")
    return render_template("home.html", user=user, message=None, today_workout=today_workout)


@app.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("login"))

    data = load_data()
    g_workouts = data.get("G", {})
    a_workouts = data.get("A", {})

    return render_template("history.html", g_workouts=g_workouts, a_workouts=a_workouts)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Prevent back button from going back to login page after login
@app.after_request
def disable_back(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == "__main__":
    app.run(debug=True)
