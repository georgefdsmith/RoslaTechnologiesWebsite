from flask import Blueprint, Flask

login_bp = Blueprint("LoginPage", __name__, template_folder="templates")

from . import LoginPage