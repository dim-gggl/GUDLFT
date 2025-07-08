import json
from flask import Flask,render_template,request,redirect,flash,url_for
from models import Club, Competition, CompetitionPlace
from config import CLUBS_FILE, COMPETITIONS_FILE
from manager import DataManager

data_manager = DataManager()

def create_app(config=None):
    app = Flask(__name__)
    app.secret_key = 'something_special'
    if config:
        app.config.from_object(config)

    competitions = data_manager.load_competitions()
    clubs = data_manager.load_clubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        club = [
            club for club in clubs if club.email == request.form['email']
        ][0]
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )

    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClub = data_manager.get_club_by_name(club)
        foundCompetition = data_manager.get_competition_by_name(competition)
        if foundClub and foundCompetition:
            competition_place = CompetitionPlace(foundCompetition)
            foundClub.add_competition_place(competition_place)
            return render_template(
                'booking.html',
                club=foundClub,
                competition=foundCompetition,
                competitions=competitions
            )
        else:
            flash("Something went wrong-please try again")
            return render_template(
                'welcome.html', 
                club=club, 
                competitions=competitions,
                club_name=club.name
            )


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competition_name = request.form['competition']
        club_name = request.form['club']
        placesRequired = int(request.form['places'])

        competition = next(comp for comp in competitions if comp.name == competition_name)
        club = next(club_obj for club_obj in clubs if club_obj.name == club_name)

        club.remove_points(placesRequired)
        competition.remove_number_of_places(placesRequired)

        competition_place = CompetitionPlace(competition=competition)
        club.add_competition_place(competition_place)

        data_manager.save_clubs(clubs)
        data_manager.save_competitions(competitions)
        
        flash('Great-booking complete!')
        return render_template(
            'welcome.html', 
            club=club.to_dict(), 
            competitions=[comp.to_dict() for comp in competitions]
        )


    # TODO: Add route for points display


    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)