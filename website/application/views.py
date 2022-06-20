from flask import render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from .database import DataBase

# register blueprint in view
view = Blueprint("views", __name__)

# GLOBAL CONSTANTS
NAME_KEY = 'name'
MSG_LIMIT = 20

@view.route("/login", methods=["POST", "GET"])
def login():
    """
    displays main login page and saves input name in session
    :exception POST
    :return: None
    """
    # when user input a name, go to home page if input is valid
    if request.method == "POST":
        name = request.form["inputName"]
        if len(name) >= 2:
            session[NAME_KEY] = name
            flash(f'You were successfully logged in as {name}.')
            return redirect(url_for("views.home"))
        else:
            flash("Name must be longer than 1 character.")

    return render_template("login.html", **{"session": session})


@view.route("/logout")
def logout():
    """
    logs the user out and popping name from session
    :return: None
    """
    session.pop(NAME_KEY, None)
    flash("You were logged out.")
    return redirect(url_for("views.login"))


@view.route("/")
@view.route("/home")
def home():
    """
    displays home page if logged in
    :return: None
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("index.html", **{"session": session})


@view.route("/history")
def history():
    """
    gets and displays the history messages sent by current user if logged in
    :return:
    """
    if NAME_KEY not in session:
        flash("Please login before viewing message history")
        return redirect(url_for("views.login"))
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    json_messages = remove_seconds_from_messages(msgs)
    return render_template("history.html", **{"history": json_messages})


@view.route("/get_name")
def get_name():
    """
    :return: a json object storing user name
    """
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)


@view.route("/get_messages")
def get_messages():
    """
    :return: all messages stored in database
    """
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    messages = remove_seconds_from_messages(msgs)

    return jsonify(messages)

def remove_seconds_from_messages(msgs):
    """
    removes the seconds from all messages
    :param msgs: list
    :return: list
    """
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)

    return messages


def remove_seconds(msg):
    """
    :return: remove the second part from time
    """
    return msg.split(".")[0][:-3]