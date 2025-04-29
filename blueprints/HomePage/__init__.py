from flask import Blueprint

home_bp = Blueprint("HomePage", __name__, template_folder="templates")

from . import HomePage
