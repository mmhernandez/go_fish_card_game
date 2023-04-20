from flask_app.models import deck
import random

class Game:
    def __init__(self):
        self.deck = deck.Deck()
        self.player_hand = []
        self.computer_hand = []

    @classmethod
    def deal(cls):
        new_game = cls()
        # for each_card in new_game.deck.cards:
        #     print(f'{each_card.face_value} of {each_card.suit}')
        
        # use the self.deck and select a random choice
        # pop the random choice and push it into a hand (alternating between the player_hand list and the computer_hand list)
        for i in range(1,15):   # 7 cards per player
            rand_card = random.choice(new_game.deck.cards)
            rand_card_index = new_game.deck.cards.index(rand_card)
            if i % 2 == 0:
                new_game.player_hand.append(new_game.deck.cards.pop(rand_card_index))
            else:
                new_game.computer_hand.append(new_game.deck.cards.pop(rand_card_index))

        print('\n---------------------\n')
        for each_card in new_game.player_hand:
            print(f'{each_card.face_value} of {each_card.suit}')
        print('\n---------------------\n')
        for each_card in new_game.computer_hand:
            print(f'{each_card.face_value} of {each_card.suit}')

