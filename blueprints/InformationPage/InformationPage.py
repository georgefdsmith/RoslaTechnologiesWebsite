# import flask
from flask import Blueprint, Flask, render_template, request
from flask_login import login_user, current_user, LoginManager, UserMixin
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash


# import bp from __init__.py
from . import information_bp


@information_bp.route("/Information")
def information_page():
    return render_template("InformationPage.html")