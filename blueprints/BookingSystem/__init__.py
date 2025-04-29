from flask import Blueprint, Flask

booking_system_bp = Blueprint("BookingSystem", __name__, template_folder="templates")

from . import BookingPage