from flask_app import app
from flask_app.models import game
from flask import render_template, session

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/start_game")
def start_game():
    game_dict = game.Game.deal()    

    game.Game.lay_down_pairs(game_dict["player_hand"])

    session["player_hand"] = game_dict["player_hand"]
    session["computer_hand"] = game_dict["computer_hand"]
    session["remaining_deck"] = game_dict["remaining_deck"]

    return render_template("index.html")