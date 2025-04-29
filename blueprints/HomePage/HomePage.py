# import flask
from flask import Blueprint, Flask, render_template, request, url_for, redirect
from flask_login import login_user, current_user, LoginManager, UserMixin
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

# import bp from __init__.py
from . import home_bp


@home_bp.route("/", methods=["GET", "POST"])
def home_page():
    return render_template("HomePage.html")


@home_bp.route("/CarbonCalculator", methods=["GET", "POST"])
def carbon_calculator():

    if request.method == "POST":

        years_owning_car = float(request.form['years-owning-a-car'])
        type_of_housing = int(request.form['type-of-housing'])
        years_eating_meat = float(request.form['years-eating-meat'])
        long_distance_travel = int(request.form['long-distance-travel'])
        type_of_travel = float(request.form["type-of-travel"])
        age = float(request.form['age'])

        emissions_from_housing = type_of_housing * age
        emissions_from_travel = (((long_distance_travel * 52.1429) * type_of_travel) * age) + years_owning_car
        emissions_from_food = years_eating_meat

        carbon_footprint = round(emissions_from_housing + emissions_from_travel + emissions_from_food)

        flights_around_the_world = round(carbon_footprint / 5.075, 2)

        return render_template("carbon-footprint-calculator.html", carbon_footprint=carbon_footprint, flights_around_the_world=flights_around_the_world)

    return render_template("carbon-footprint-calculator.html")


@home_bp.route("/EnergyCalculator", methods=["GET", "POST"])
def energy_calculator():

    if request.method == "POST":

        hours_using_heating = float(request.form['hours-using-heating'])
        computers_owned_in_household = float(request.form['computers-owned-in-household'])
        hours_running_lights = float(request.form['hours-running-lights'])
        amount_of_fridges = float(request.form['amount-of-fridges'])
        amount_of_freezers = float(request.form['amount-of-freezers'])
        washing_machines = float(request.form['washing-machines'])
        tumble_dryer = float(request.form['tumble-dryer'])
        dishwasher = float(request.form['dishwasher'])
        type_of_housing = float(request.form['type-of-housing'])

        cost_of_heating = hours_using_heating * type_of_housing
        cost_of_appliances = computers_owned_in_household
        cost_of_appliances += hours_running_lights * type_of_housing
        cost_of_appliances += amount_of_freezers + amount_of_fridges + washing_machines + tumble_dryer + dishwasher

        daily_energy_cost = round(cost_of_heating + cost_of_appliances, 2)

        return render_template("energy-tracking-calculator.html", energy_cost=daily_energy_cost)

    return render_template("energy-tracking-calculator.html")
