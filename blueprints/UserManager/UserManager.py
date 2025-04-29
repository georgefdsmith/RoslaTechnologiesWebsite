# import flask
import datetime
import sqlite3

from flask import Blueprint, Flask, render_template, request, url_for, redirect, session
from flask_login import login_user, current_user, LoginManager, UserMixin, login_required, logout_user
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest

# import bp from __init__.py
from . import user_manager_bp


class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.user_id)


@user_manager_bp.route("/Account", methods=["GET", "POST"])
def Account():

    conn = sqlite3.connect("Rosla_Technologies_Database.db")
    c = conn.cursor()

    if current_user.is_authenticated:
        user_id = current_user.user_id

        c.execute("SELECT username, address, name FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()

        conn.commit()

        c.execute("SELECT * FROM bookedServices WHERE user_id = ?", (user_id,))
        booked_services = c.fetchall()

    if request.method == "POST":

        page_redirect = request.form['page-redirect']

        return redirect(url_for(page_redirect))


@user_manager_bp.route("/change_account_details", methods=["GET", "POST"])
def change_account_details():

    conn = sqlite3.connect("Rosla_Technologies_Database.db")
    c = conn.cursor()

    user_id = current_user.user_id

    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()

    conn.commit()

    if request.method == "POST":

        try:

            gateway_password = request.form['gateway_password']

            if check_password_hash(user[2], gateway_password):

                return render_template("ChangeAccountDetailsPage.html", username=user[1], password=gateway_password, address=user[3], name=user[4])

            elif not check_password_hash(user[2], gateway_password):

                flash = "Error incorrect password"
                return render_template("ChangeAccountDetailsPageGateway.html", flash=flash)

        except KeyError:

            username = request.form['username']
            password = request.form['password']
            address = request.form['address']
            name = request.form['name']

            hashed_password = generate_password_hash(password).decode("utf-8")

            c.execute("UPDATE users SET username = ?, password = ?, address = ?, name = ? WHERE id = ?", (username, hashed_password, address, name, user_id))

            conn.commit()

            return redirect(url_for("HomePage.home_page"))

    return render_template("ChangeAccountDetailsPageGateway.html")


@user_manager_bp.route("/change_booked_appointments", methods=["GET", "POST"])
def change_booked_appointments():

    conn = sqlite3.connect("Rosla_Technologies_Database.db")
    c = conn.cursor()

    user_id = current_user.user_id

    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()

    c.execute("SELECT * FROM bookedServices WHERE user_id = ?", (user_id,))
    booked_services = c.fetchall()

    c.execute("SELECT appointment_id, datetime FROM bookedServices")
    all_dates = c.fetchall()

    today = str(datetime.datetime.now())[5:10]

    # deletes appointments in the past
    for x in range(len(all_dates)):

        print(int(all_dates[x][1][:2]) - 2, int(today[3:]), int(today[:2]), int(all_dates[x][1][3:]) + 1)    

        if int(all_dates[x][1][:2]) < int(today[3:]) and int(all_dates[x][1][3:]) < int(today[:2]):
            
            c.execute("DELETE FROM bookedServices WHERE appointment_id = ?", (all_dates[x][0],))

            conn.commit()

            return redirect(url_for("UserManager.change_booked_appointments"))

    if request.method == "POST":

        i = request.form['index']

        i = int(i)

        return redirect(url_for("BookingSystem.change_booking", appointment_id=booked_services[i][0], current_selected_date=booked_services[i][1]))

    return render_template("ChangeBookedAppointmentsPage.html", booked_services=booked_services, )


@user_manager_bp.route("/delete_booked_appointments", methods=["GET", "POST"])
def delete_booked_appointments():

    conn = sqlite3.connect("Rosla_Technologies_Database.db")
    c = conn.cursor()

    user_id = current_user.user_id

    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()

    c.execute("SELECT * FROM bookedServices WHERE user_id = ?", (user_id,))
    booked_services = c.fetchall()

    if request.method == "POST":

        i = request.form['delete_index']

        i = int(i)

        appointment_id = booked_services[i][0]

        c.execute("DELETE FROM bookedServices WHERE appointment_id = ?", (appointment_id,))

        conn.commit()

        return redirect(url_for("UserManager.change_booked_appointments"))

    return render_template("ChangeBookedAppointmentsPage.html", booked_services=booked_services)


@user_manager_bp.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("HomePage.home_page"))


@user_manager_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("HomePage.home_page"))