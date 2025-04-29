# import flask
from flask import Blueprint, Flask, render_template, request, url_for, redirect
from flask_login import login_user, current_user, LoginManager, UserMixin
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

# import module for databases
import sqlite3


# import flask blueprints
from blueprints.BookingSystem import booking_system_bp
from blueprints.HomePage import home_bp
from blueprints.InformationPage import information_bp
from blueprints.LoginPage import login_bp
from blueprints.RegisterPage import register_bp
from blueprints.UserManager import user_manager_bp


# init flask app
app = Flask("__name__")


# init bcrypt
app.secret_key = "secret_key"
bcrypt = Bcrypt(app)


# init login manager
login_manager = LoginManager(app)
login_manager.init_app(app)


# init flask blueprints
app.register_blueprint(booking_system_bp, url_prefix="/BookingSystem")
app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(information_bp, url_prefix="/InformationPage")
app.register_blueprint(login_bp, url_prefix="/LoginAccount")
app.register_blueprint(register_bp, url_prefix="/RegisterAccount")
app.register_blueprint(user_manager_bp, url_prefix="/UserManager")


# function for schema storage and database creation
def create_database():
    conn = sqlite3.connect("Rosla_Technologies_Database.db")
    c = conn.cursor()

    c.execute(''' CREATE TABLE IF NOT EXISTS users 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        address TEXT NOT NULL,
        name TEXT NOT NULL
    )   
    ''')

    conn.commit()

    c.execute('''
    CREATE TABLE IF NOT EXISTS bookedServices 
    (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT NOT NULL,
        serviceBooked TEXT NOT NULL,
        description TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        user_address TEXT NOT NULL
    )
    ''')

    conn.commit()

    conn.close()


# user_loader is required for the account system to work
# this function needs to return None for no user or a user object if user is detected
@login_manager.user_loader
def load_user(user_id):
    # import User class here to avoid circular import
    from blueprints.UserManager.UserManager import User

    # connect to database
    conn = sqlite3.connect("Rosla_Technologies_Database.db")
    c = conn.cursor()

    # execute sql command
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    fetched_user = c.fetchone()

    # returning None for no user
    if fetched_user is None:
        return

    # returns user object
    else:
        return User(int(fetched_user[0]), fetched_user[1])


if __name__ == "__main__":
    create_database()
    app.run(host='0.0.0.0', port=3000, debug=True)
