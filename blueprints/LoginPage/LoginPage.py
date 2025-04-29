# import flask
from flask import Blueprint, Flask, render_template, request, url_for, redirect
from flask_login import login_user, current_user, LoginManager, UserMixin
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

# import module for databases
import sqlite3

# import bp from __init__.py
from . import login_bp

# import User class from UserManager.py for login
from blueprints.UserManager.UserManager import User

bcrypt = Bcrypt()


@login_bp.route("/Login", methods=["GET", "POST"])
def login_page():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("Rosla_Technologies_Database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()

        if user is not None:
            if user[1] == username and check_password_hash(user[2], password):
                login_user(User(user[0], user[1]))
                return redirect(url_for("HomePage.home_page"))
        else:
            flash = "No Account Detected, did you mean Register?"
            return render_template("LoginPage.html", flash=flash)

        conn.commit()
        conn.close()

    return render_template("LoginPage.html")