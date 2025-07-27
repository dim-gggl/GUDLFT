
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
    process_data_persistance_during_booking,
    CLUBS,
    COMPETITIONS
)


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
    return render_template("index.html")

@app.route("/show_summary", methods=["POST"])
def show_summary():    
    club = get_obj_by_field("email", request.form["email"], CLUBS)
    return render_template("welcome.html", 
                            club=club, 
                            competitions=COMPETITIONS)


@app.route("/book/<competition>/<club>")
def book(competition_name, club_name):
    club = get_obj_by_field("name", club_name, CLUBS)
    competition = get_obj_by_field("name", 
                                    competition_name, 
                                    COMPETITIONS)
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

@app.route("/purchase_places", methods=["POST"])
def purchase_places():

    competition = get_obj_by_field("name", 
                                    request.form["competition"], 
                                    COMPETITIONS)
    club = get_obj_by_field("name", request.form["club"], CLUBS)
    places_required = int(request.form["places"])
    
    error = process_data_persistance_during_booking(competition, 
                                                    club, 
                                                    places_required)
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

@app.route("/display_points")
def display_points():
    """Display the points of the clubs from the main page"""
    if not CLUBS:
        flash("No clubs found")
        return render_template("welcome.html")
    return render_template("points.html", clubs=CLUBS)

@app.route("/logout")
def logout():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)