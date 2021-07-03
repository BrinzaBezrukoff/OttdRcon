from flask import *
from flask_login import login_required, current_user, login_user, logout_user

from app import app, sessions_manager
from models import User


@app.route("/")
def index():
    return redirect(url_for("panel"))


@app.route("/panel")
@login_required
def panel():
    session = sessions_manager.new_session(current_user)
    return render_template("panel.html", token=session.token)


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
        return jsonify({"result": False, "message": "invalid_auth_data"})
    login_user(u)
    return jsonify({"result": True})


@app.route("/ajax/update", methods=["POST"])
@login_required
@sessions_manager.session_required
def ajax_update_console(session):
    return jsonify({"result": True, "text": session.client.console})


@app.route("/ajax/command_send", methods=["POST"])
@login_required
@sessions_manager.session_required
def ajax_command_send(session):
    j = request.get_json()
    command = j.get("command")
    if not command:
        return jsonify({"result": False, "message": "command_not_passed"})
    session.client.send_command(command)
    return jsonify({"result": True})
