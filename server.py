from flask import (
    Flask, 
    render_template, 
    request,
    redirect, 
    flash, 
    url_for
)

from config import config
from data_manager import (
    get_obj_by_field, 
    update_data_after_booking,
    CLUBS,
    COMPETITIONS
)
from validators import mail_is_unknown


########################################################
# FLASK APP FACTORY & INITIALIZATION
########################################################

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config["default"])
    app.secret_key = app.config["SECRET_KEY"]
    return app

app = create_app()


########################################################
# FLASK ROUTES
########################################################

@app.route("/")
def index():
    """Display the main page"""
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():    
    """
    Display the welcome page with the club's information
    and the competitions list.
    """
    email = request.form.get("email")
    if mail_is_unknown(email, CLUBS):
        flash("Please enter a valid email")
        return redirect(url_for("index"))
    
    else:
        club = get_obj_by_field("email", email, CLUBS)
        return render_template("welcome.html", 
                                club=club, 
                                competitions=COMPETITIONS)


@app.route("/book/<competition_name>/<club_name>")
def book(competition_name, club_name):
    """Display the booking page"""
    try:
        club = get_obj_by_field("name", club_name, CLUBS)
        competition = get_obj_by_field("name", competition_name, COMPETITIONS)
        
        if club and competition:
            return render_template(
                "booking.html",
                club=club,
                competition=competition
            )
        else:
            flash("Something went wrong-please try again")
            return render_template(
                "welcome.html", 
                club=club, 
                competitions=COMPETITIONS
            )
    except IndexError:
        flash("Invalid competition or club")
        return redirect(url_for("index"))


@app.route("/purchase_places", methods=["POST"])
def purchase_places():
    """
    Display and process the booking of places for a 
    competition by a club.
    """
    try:
        competition_name = request.form.get("competition")
        club_name = request.form.get("club")
        places_str = request.form.get("places")
        
        if not all([competition_name, club_name, places_str]):
            flash("Missing required data")
            return redirect(url_for("index"))
            
        competition = get_obj_by_field("name", competition_name, COMPETITIONS)
        club = get_obj_by_field("name", club_name, CLUBS)
        places_required = int(places_str)
        
        error = update_data_after_booking(competition, club, places_required)
        if error:
            flash(error)
            return render_template(
                "booking.html",
                club=club,
                competition=competition
            )
        else:
            flash("Great-booking complete!")
            return render_template("welcome.html", 
                                    club=club, 
                                    competitions=COMPETITIONS)
    except (ValueError, IndexError, KeyError):
        flash("Invalid data provided")
        return redirect(url_for("index"))


@app.route("/display_points")
def display_points():
    """Display the points of the clubs from the main page"""
    return render_template("points.html", clubs=CLUBS)


@app.route("/logout")
def logout():
    """Redirect to the main page"""
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)