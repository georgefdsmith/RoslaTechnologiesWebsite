from flask import Blueprint

register_bp = Blueprint("RegisterPage", __name__, template_folder="templates")

from . import RegisterPage