from flask_app import app
from flask_app.models import game
from flask import render_template, session, redirect, request


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/start_game")
def start_game():
    if "game_over" in session:
        session.clear()

    game_dict = game.Game.deal()    
    session["player_hand"] = game_dict["player_hand"]
    session["computer_hand"] = game_dict["computer_hand"]
    session["deck"] = game_dict["deck"]
    message = "The game has begun, and you're up first!"

    hasPairs = game.Game.check_for_pairs(game_dict["player_hand"])
    return render_template("index.html", message=message, hasPairs=hasPairs)


@app.route("/pairs", methods=["POST"])
def lay_down_pairs():
    # confirm player is attempting to lay down a pair (2 cards only)
    if len(request.form) != 2:
        message = "Select a pair (2) of cards with the same face value."
        return render_template("index.html", message=message, hasPairs=True, color="red")
    
    # grab the pair of cards from the request form
    req_form_pairs = []
    for each in request.form:
        req_form_pairs.append(each)
    # format pair for logic
    card1_dict = {
        "suit": req_form_pairs[0][:1],
        "face_value": req_form_pairs[0][1:]
    }  
    card2_dict = {
        "suit": req_form_pairs[1][:1],
        "face_value": req_form_pairs[1][1:]
    }
    pair_list = []
    pair_list.append(card1_dict)
    pair_list.append(card2_dict)
    
    # confirm player attempted to lay down a pair of matching cards 
    if card1_dict["face_value"] != card2_dict["face_value"]:
        message = "Pairs of cards must have the same face value."
        return render_template("index.html", message=message, hasPairs=True, color="red")

    # if the pair is valid, proceed with setting session variables and calling lay_down_pairs method
    player_hand = session["player_hand"]
    deck = session["deck"]

    # do not allow duplication of cards when player refreshes and resubmits the form
    if "player_pairs" in session:
        hasPairs = game.Game.check_for_pairs(player_hand)
        player_pairs = session["player_pairs"]
        for i in range(len(player_pairs)):
            for j in range(len(pair_list)):
                if player_pairs[i]["suit"] == pair_list[j]["suit"] and player_pairs[i]["face_value"] == pair_list[j]["face_value"]:
                    return render_template("index.html", hasPairs=hasPairs)

    # lay down the pair selected and draw from the deck
    updated_player_game_dict = game.Game.lay_down_pairs(player_hand, pair_list, deck)
    session["player_hand"] = updated_player_game_dict["hand"]
    if "player_pairs" in session:
        player_pairs.extend(updated_player_game_dict["pairs"])
        session["player_pairs"] = player_pairs
    else:
        session["player_pairs"] = updated_player_game_dict["pairs"]
    
    # game over check
    if "player_pairs" in session and "computer_pairs" in session:
        game_check_result = game.Game.game_over_check(session["player_hand"], session["player_pairs"], session["computer_hand"], session["computer_pairs"])
    elif "player_pairs" in session and not "computer_pairs" in session:
        computer_pairs = []
        game_check_result = game.Game.game_over_check(session["player_hand"], session["player_pairs"], session["computer_hand"], computer_pairs)
    elif not "player_pairs" in session and "computer_pairs" in session:
        player_pairs = []
        game_check_result = game.Game.game_over_check(session["player_hand"], player_pairs , session["computer_hand"], session["computer_pairs"])
    else:
        player_pairs = []
        computer_pairs = []
        game_check_result = game.Game.game_over_check(session["player_hand"], player_pairs, session["computer_hand"], computer_pairs)

    if game_check_result["game_over_flag"]:
        return render_template("index.html", game_over=game_check_result)
    
    hasPairs = game.Game.check_for_pairs(updated_player_game_dict["hand"])
    return render_template("index.html", hasPairs=hasPairs)


@app.route("/draw")
def draw_card():
    player_hand = session["player_hand"]
    deck = session["deck"]

    updated_cards = game.Game.draw_from_deck(player_hand, deck)
    session["player_hand"] = updated_cards["hand"]
    session["deck"] = updated_cards["deck"]

    hasPairs = game.Game.check_for_pairs(updated_cards["hand"])
    return render_template("index.html", hasPairs=hasPairs)


@app.route("/request/<int:point_value>")
def card_request(point_value):
    player_hand = session["player_hand"]
    computer_hand = session["computer_hand"]
    deck = session["deck"]

    # check computer hand for requested card's point value
    result = game.Game.check_hand_for_card(player_hand, computer_hand, point_value, deck)

    # if the computer doesn't have a match, the computer will take a turn
    if not result["hasMatch"]:
        message = "The computer did not have a matching card. Your turn is over and the computer will take a turn."

        player_hand = result["request_hand"]
        computer_hand = result["check_hand"]
        deck = result["deck"]

        if "computer_pairs" in session:
            computer_pairs = session["computer_pairs"]
        else:
            computer_pairs = []

        computer_turn_result = game.Game.computer_turn(computer_hand, computer_pairs, player_hand, deck)

        session["player_hand"] = computer_turn_result["player_hand"]
        session["computer_hand"] = computer_turn_result["computer_hand"]
        session["deck"] = computer_turn_result["deck"]
        if len(computer_pairs) > 0:
            session["computer_pairs"] = computer_turn_result["computer_pairs"]

        # game over check
        if "player_pairs" in session and "computer_pairs" in session:
            game_check_result = game.Game.game_over_check(session["player_hand"], session["player_pairs"], session["computer_hand"], session["computer_pairs"])
        elif "player_pairs" in session and not "computer_pairs" in session:
            computer_pairs = []
            game_check_result = game.Game.game_over_check(session["player_hand"], session["player_pairs"], session["computer_hand"], computer_pairs)
        elif not "player_pairs" in session and "computer_pairs" in session:
            player_pairs = []
            game_check_result = game.Game.game_over_check(session["player_hand"], player_pairs , session["computer_hand"], session["computer_pairs"])
        else:
            player_pairs = []
            computer_pairs = []
            game_check_result = game.Game.game_over_check(session["player_hand"], player_pairs, session["computer_hand"], computer_pairs)

        if game_check_result["game_over_flag"]:
            return render_template("index.html", game_over=game_check_result)

        hasPairs = game.Game.check_for_pairs(computer_turn_result["player_hand"])

    # if the computer has a matching point value card, pass to the player's hand
    else:
        message = "The computer had a match!"
        computer_draw_dict = game.Game.draw_from_deck(result["check_hand"], result["deck"])

        session["player_hand"] = result["request_hand"]
        session["computer_hand"] = computer_draw_dict["hand"]
        session["deck"] = computer_draw_dict["deck"]
        hasPairs = game.Game.check_for_pairs(result["request_hand"])
        
    return render_template("index.html", hasPairs=hasPairs, message=message)


@app.route("/clear")
def clear_game_session():
    session.clear()
    return redirect("/")