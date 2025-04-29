# import flask
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask_login import login_user, current_user, LoginManager, UserMixin
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash


#import module for database
import sqlite3


#import bp from __init__.py
from . import register_bp


#init bcrypt
bcrypt = Bcrypt()


@register_bp.route("/Register", methods=["GET", "POST"])
def register_page():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        address = request.form["address"]
        name = request.form["name"]

        encrypted_password = generate_password_hash(password).decode("utf-8")

        conn = sqlite3.connect("Rosla_Technologies_Database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_users = c.fetchall()

        empty_arr = []

        if existing_users != empty_arr:

            print("user detected ")

            flash = "user already exists did you mean login?"

            return render_template("RegisterPage.html", flash=flash)

        c.execute("INSERT INTO users (username, password, address, name) VALUES (?, ?, ?, ?)", (username, encrypted_password, address, name))

        conn.commit()
        conn.close()

        return redirect(url_for("LoginPage.login_page"))

    return render_template("RegisterPage.html")