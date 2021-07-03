from flask import *
from flask_login import login_required, current_user, login_user, logout_user

from app import app
from models import User
from ottd import client


@app.route("/")
def index():
    return redirect(url_for("panel"))


@app.route("/panel")
@login_required
def panel():
    return render_template("panel.html")


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("panel"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.errorhandler(401)
def error_401(error):
    return redirect(url_for("login"))


# AJAX handlers


@app.route("/ajax/login", methods=["POST"])
def ajax_login():
    if current_user.is_authenticated:
        return jsonify({"result": True})

    j = request.get_json()
    username, password = j["username"], j["password"]
    u = User.query.filter(User.username == username).first()
    if not u:
        return jsonify({"result": False, "message": "user_not_found"})
    if not u.check_password(password):
        return jsonify({"result": False, "message": "incorrect_data"})
    login_user(u)
    return jsonify({"result": True})


@app.route("/ajax/update")
@login_required
def ajax_update_console():
    return jsonify({"text": client.console})


@app.route("/ajax/command_send", methods=["POST"])
@login_required
def ajax_command_send():
    command = request.get_json().get("command")
    if not command:
        return jsonify({"result": False})
    client.send_command(command)
    return jsonify({"result": True})
