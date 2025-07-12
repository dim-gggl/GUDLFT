import json
import os
from flask import Flask, render_template, request,redirect, flash, url_for

from config import config


def load_json(file_path, key):
    with open(file_path) as f:
        return json.load(f)[key]

def save_json(file_path, data, key):
    with open(file_path, "w") as f:
        json.dump({key: data}, f)

def save_clubs_and_competitions(clubs, competitions):
    save_json(app.config["JSON_CLUBS"], clubs, "clubs")
    save_json(app.config["JSON_COMPETITIONS"], competitions, "competitions")

def create_app(conf='default'):
    app = Flask(__name__)
    cfg = os.environ.get('FLASK_ENV', conf)
    app.config.from_object(config[cfg])

    app.secret_key = app.config["SECRET_KEY"]

    return app


app = create_app()

competitions = load_json(
    app.config["JSON_COMPETITIONS"],
    "competitions"
)
clubs = load_json(app.config["JSON_CLUBS"], "clubs")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points'])-placesRequired
    save_clubs_and_competitions(clubs, competitions)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)