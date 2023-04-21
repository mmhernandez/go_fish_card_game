from flask_app.models import deck
import random
from collections import Counter

class Game:
    def __init__(self):
        self.deck = deck.Deck()
        self.player_hand = []
        self.computer_hand = []

    @classmethod
    def deal(cls):
        new_game = cls()

        # deal the cards from the deck to each player
        for i in range(1,15):   # 7 cards per player            
            rand_card = random.choice(new_game.deck.cards)
            rand_card_index = new_game.deck.cards.index(rand_card)
            new_game.deck.cards.pop(rand_card_index)

            rand_card_dict = {
                "suit": rand_card.suit,
                "face_value": rand_card.face_value,
                "point_value": rand_card.point_value
            }
            # alternate dealing cards to each player
            if i % 2 == 0:
                new_game.player_hand.append(rand_card_dict)
            else:
                new_game.computer_hand.append(rand_card_dict)

        remaining_deck = []
        for each_card in new_game.deck.cards:
            card_dict = {
                "suit": each_card.suit,
                "face_value": each_card.face_value,
                "point_value": each_card.point_value
            }
            remaining_deck.append(card_dict)

        game_dict = {
            "player_hand": new_game.player_hand,
            "computer_hand": new_game.computer_hand,
            "remaining_deck": remaining_deck
        }
        return game_dict
    

    @classmethod
    def lay_down_pairs(cls, hand):
        pairs = []
        lookup_dict = {}

        for i in range(len(hand)):
            lookup_dict[i] = hand[i]["point_value"]

        print(lookup_dict)

        # create a counter from the dictionary values
        counts = Counter(lookup_dict.values())

        #create a new list with only the keys (i.e. indecies) with count(values) > 1
        pairs_index_list = [k for k,v in lookup_dict.items() if counts[v] % 2 == 0]
        
        print(pairs_index_list)
