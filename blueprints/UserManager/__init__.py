from flask import Blueprint

user_manager_bp = Blueprint("UserManager", __name__, template_folder="templates")

from . import UserManager
