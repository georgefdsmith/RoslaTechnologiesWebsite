# import flask
import datetime

from flask import Blueprint, Flask, render_template, request, url_for, redirect
from flask_login import login_user, current_user, LoginManager, UserMixin, login_required
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

# import module for databases
import sqlite3

# import bp from __init__.py
from . import booking_system_bp


@booking_system_bp.route("/Book", methods=["GET", "POST"])
@login_required
def booking_system_calender():
    conn = sqlite3.connect("Rosla_Technologies_Database.db")
    c = conn.cursor()

    c.execute("SELECT datetime FROM bookedServices")
    booked_dates = c.fetchall()

    conn.commit()

    for i in range(len(booked_dates)):
        booked_dates[i] = booked_dates[i][0]

    today = str(datetime.datetime.now())[5:10]

    days_in_month_array = [31,28,31,30,31,30,31,31,30,31,30,31]
    week_days = ["M", "T", "W", "T", "F", "S", "S"]

    selected_month = int(request.args.get('month', int(str(datetime.datetime.now())[5:7]) - 1))

    if request.method == "POST":
        date_time = request.form['selected_day']
        user_id = current_user.user_id

        print(date_time)

        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()

        user_name = user[4]
        user_address = user[3]

        return redirect(url_for("BookingSystem.booking_system_form", date_time=date_time, user_id=user_id, user_name=user_name, user_address=user_address))

    return render_template("BookingSystemPage.html", days_in_month_array=days_in_month_array, week_days=week_days, selected_month=selected_month, booked_dates=booked_dates, today=today)


@booking_system_bp.route("/Form/<date_time>/<user_id>/<user_name>/<user_address>", methods=["GET", "POST"])
def booking_system_form(date_time, user_id, user_name, user_address):

    if request.method == "POST":

        service = request.form["service-button"]
        description = request.form['description']

        conn = sqlite3.connect("Rosla_Technologies_Database.db")
        c = conn.cursor()

        c.execute("INSERT INTO bookedServices (datetime, serviceBooked, description, user_id, user_name, user_address) VALUES (?,?,?,?,?,?)", (date_time, service, description, user_id, user_name, user_address,))

        conn.commit()

        return redirect(url_for("HomePage.home_page"))

    return render_template("BookingSystemForm.html", date_time=date_time, user_id=user_id, user_name=user_name, user_address=user_address)


@booking_system_bp.route("/ChangeBooking/<appointment_id>/<current_selected_date>", methods=["GET", "POST"])
@login_required
def change_booking(appointment_id,current_selected_date):
    conn = sqlite3.connect("Rosla_Technologies_Database.db")
    c = conn.cursor()

    c.execute("SELECT datetime FROM bookedServices")
    booked_dates = c.fetchall()

    conn.commit()

    for i in range(len(booked_dates)):
        booked_dates[i] = booked_dates[i][0]

    today = str(datetime.datetime.now())[5:10]

    days_in_month_array = [31,28,31,30,31,30,31,31,30,31,30,31]
    week_days = ["M", "T", "W", "T", "F", "S", "S"]

    selected_month = int(request.args.get('month', int(str(datetime.datetime.now())[5:7]) - 1))

    if request.method == "POST":
        date_time = request.form['selected_day']
        user_id = current_user.user_id

        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()

        user_name = user[4]
        user_address = user[3]

        return redirect(url_for("BookingSystem.change_appointment_form", current_selected_date=current_selected_date, appointment_id=appointment_id, date_time=date_time, user_id=user_id, user_name=user_name, user_address=user_address))

    return render_template("ChangeAppointmentPage.html", current_selected_date=current_selected_date, appointment_id=appointment_id, days_in_month_array=days_in_month_array, week_days=week_days, selected_month=selected_month, booked_dates=booked_dates, today=today)


@booking_system_bp.route("/ChangeAppointmentForm/<current_selected_date>/<appointment_id>/<date_time>/<user_id>/<user_name>/<user_address>", methods=["GET", "POST"])
def change_appointment_form(current_selected_date, appointment_id, date_time, user_id, user_name, user_address):

    if request.method == "POST":

        service = request.form["service-button"]
        description = request.form['description']

        conn = sqlite3.connect("Rosla_Technologies_Database.db")
        c = conn.cursor()

        c.execute("UPDATE bookedServices SET datetime = ?, serviceBooked = ?, description = ?, user_name = ?, user_address = ? WHERE appointment_id = ?", (date_time, service, description, user_name, user_address, appointment_id))

        conn.commit()

        return redirect(url_for("HomePage.home_page"))

    return render_template("ChangeAppointmentForm.html", current_selected_date=current_selected_date, appointment_id=appointment_id, date_time=date_time, user_id=user_id, user_name=user_name, user_address=user_address)