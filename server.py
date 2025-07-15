import json
import os
from flask import (
    Flask, 
    render_template, 
    request,
    redirect, 
    flash, 
    url_for, 
    current_app
)

from config import config
from validators import validate_places_required, validate_competition_date


def load_json(file_path, key):
    """Load JSON data from a club or competition file"""
    with open(file_path) as f:
        return json.load(f)[key]

def save_json(file_path, data, key):
    """Save JSON data to a club or competition file"""
    with open(file_path, "w") as f:
        json.dump({key: data}, f, ensure_ascii=True, indent=4)

def save_clubs_and_competitions(app_instance, clubs, competitions):
    """Save clubs and competitions to their respective files"""
    save_json(app_instance.config["JSON_CLUBS"], clubs, "clubs")
    save_json(
        app_instance.config["JSON_COMPETITIONS"], 
        competitions, 
        "competitions"
    )

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config["default"])
    app.secret_key = app.config["SECRET_KEY"]
    return app

def dict_from_list(key, value, list_of_dicts):
    return [item for item in list_of_dicts if item[key] == value][0]

app = create_app()

clubs = load_json(app.config["JSON_CLUBS"], "clubs")
competitions = load_json(app.config["JSON_COMPETITIONS"], "competitions")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/show_summary",methods=["POST"])
def show_summary():    
    club = dict_from_list("email", request.form["email"], clubs)
    return render_template("welcome.html",club=club,competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = dict_from_list("name", club, clubs)
    found_competition = dict_from_list("name", competition, competitions)
    if found_club and found_competition:
        return render_template(
            "booking.html",
            club=found_club,
            competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", 
            club=club, 
            competitions=competitions
        )

@app.route("/purchase_places",methods=["POST"])
def purchase_places():
    current_competitions = load_json(
        current_app.config["JSON_COMPETITIONS"], 
        "competitions"
    )
    current_clubs = load_json(current_app.config["JSON_CLUBS"], "clubs")
    
    competition = dict_from_list("name", request.form["competition"], current_competitions)
    club = dict_from_list("name", request.form["club"], current_clubs)

    places_required = int(request.form["places"])
    reservation_error = validate_places_required(places_required, club, competition)
    date_error = validate_competition_date(competition)
    error = reservation_error or date_error
    if error:
        flash(error)
        return render_template(
            "booking.html",
            club=club,
            competition=competition
        )
    

    competition["number_of_places"] = int(competition["number_of_places"]) \
        - places_required
    club["points"] = int(club["points"]) - places_required

    
    save_clubs_and_competitions(
        current_app, 
        current_clubs, 
        current_competitions
    )
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=current_competitions)

@app.route("/display_points")
def display_points():
    """Display the points of the clubs from the main page"""
    return render_template("points.html", clubs=clubs)

@app.route("/logout")
def logout():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)