from flask_app import app
from flask_app.models import game
from flask import render_template

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/start_game")
def start_game():
    game.Game.deal()
    return ("Game started...")