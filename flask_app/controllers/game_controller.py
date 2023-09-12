from flask_app import app
from flask_app.models import game
from flask import render_template, session, redirect, request


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/start_game")
def start_game():
    game_dict = game.Game.deal()    
    session["player_hand"] = game_dict["player_hand"]
    session["computer_hand"] = game_dict["computer_hand"]
    session["deck"] = game_dict["deck"]
    message = "The game has begun, and it's your turn!"

    hasPairs = game.Game.check_for_pairs(game_dict["player_hand"])

    return render_template("index.html", message=message, hasPairs=hasPairs)


@app.route("/pairs", methods=["POST"])
def lay_down_pairs():
    # confirm player is attempting to lay down a pair (2 cards only)
    if len(request.form) != 2:
        message = "Select a pair (2) of cards with the same face value."
        return render_template("index.html", message=message)
    
    pair_list = []
    for each in request.form:
        pair_list.append(each)
    card1_dict = {
        "suit": pair_list[0][:1],
        "face_value": pair_list[0][1:]
    }  
    card2_dict = {
        "suit": pair_list[1][:1],
        "face_value": pair_list[1][1:]
    }  
    # confirm player attempted to lay down a pair of matching cards 
    if card1_dict["face_value"] != card2_dict["face_value"]:
        message = "Pairs of cards must have the same face value."
        return render_template("index.html", message=message, color="red")

    # if the pair is valid, proceed with setting session variables and calling lay_down_pairs method
    player_hand = session["player_hand"]
    computer_hand = session["computer_hand"]
    deck = session["deck"]

    if "player_pairs" in session:
        player_pairs = session["player_pairs"]
    if "computer_pairs" in session:
        computer_pairs = session["computer_pairs"]

    updated_player_game_dict = game.Game.lay_down_pairs(player_hand, deck)
    session["player_hand"] = updated_player_game_dict["hand"]
    if "player_pairs" in session:
        player_pairs.extend(updated_player_game_dict["pairs"])
        session["player_pairs"] = player_pairs
    else:
        session["player_pairs"] = updated_player_game_dict["pairs"]

    updated_computer_game_dict = game.Game.lay_down_pairs(computer_hand, updated_player_game_dict["deck"])
    session["computer_hand"] = updated_computer_game_dict["hand"]
    if "computer_pairs" in session:
        computer_pairs.extend(updated_computer_game_dict["pairs"])
        session["computer_pairs"] = computer_pairs
    else:
        session["computer_pairs"] = updated_computer_game_dict["pairs"]

    session["deck"] = updated_computer_game_dict["deck"]
    
    hasPairs = game.Game.check_for_pairs(updated_player_game_dict["hand"])
    
    return render_template("index.html", message=message, hasPairs=hasPairs)


@app.route("/request/<int:point_value>")
def card_request(point_value):
    player_hand = session["player_hand"]
    computer_hand = session["computer_hand"]
    deck = session["deck"]

    result = game.Game.check_hand_for_card(player_hand, computer_hand, point_value, deck)

    if not result["flag"]:
        message = "The computer did not have a matching card and has taken it's turn."

        player_hand = result["request_hand"]
        computer_hand = result["check_hand"]
        deck = result["deck"]

        computer_turn_result = game.Game.computer_turn(computer_hand, player_hand, deck)

        session["player_hand"] = computer_turn_result["request_hand"]
        session["computer_hand"] = computer_turn_result["check_hand"]
        session["deck"] = computer_turn_result["deck"]
        hasPairs = game.Game.check_for_pairs(computer_turn_result["check_hand"])

    else:
        message = "The computer had a match!"
        session["player_hand"] = result["request_hand"]
        session["computer_hand"] = result["check_hand"]
        session["deck"] = result["deck"]
        hasPairs = game.Game.check_for_pairs(result["request_hand"])
        
    return render_template("index.html", hasPairs=hasPairs, message=message)


@app.route("/clear")
def clear_game_session():
    session.clear()
    return redirect("/")