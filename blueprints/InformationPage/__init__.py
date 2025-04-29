from flask import Blueprint, Flask

information_bp = Blueprint("InformationPage", __name__, template_folder="templates")

from . import InformationPage