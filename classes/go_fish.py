from classes.deck import Deck
import random

class Go_Fish:
    def __init__(self, player1_name, player2_name):
        self.player1 = player1_name
        self.player2 = player2_name
        self.game_deck = Deck() #create copy of full deck
        self.player1_hand = []
        self.player2_hand = []
        
    def start_game(self):
        self.player1_hand = self.deal_cards()
        self.show_player_hand(self.player1)
        self.lay_down_pairs(self.player1_hand)

        self.player2_hand = self.deal_cards()
        self.show_player_hand(self.player2)
        self.lay_down_pairs(self.player2_hand)

        print("Let's play Go-Fish!")
        self.player_turn(self.player1, self.player2)
    
    def deal_cards(self):
        hand = []
        while len(hand) < 10:
            card = self.draw_card()
            # print(f"{card.string_val} of {card.suit}")
            hand.append(card)
            self.remove_card_from_deck(card)
        return hand
    
    def remove_card_from_deck(self, card):
        index = 0
        for i in self.game_deck.cards: 
            if i == card:
                self.game_deck.cards.pop(index)
                return self
            else:
                index += 1
    
    def draw_card(self):
        return random.choice(self.game_deck.cards)
    
    def lay_down_pairs(self, hand):
        #loop through the player's hand and "lay down" (i.e. remove) any pairs from their hand
        card_value_dict = {}
        dupe_cards_to_remove = []
        count = 2
        for card in hand:
            if card.string_val == str(count):
                card_value_dict[card.string_val] += 1
            count += 1

        print(card_value_dict)
        print(dupe_cards_to_remove)
        return self

    def player_turn(self, current_player, other_player):
        card_ask = input(f"Enter the word 'hand' to view your current hand.\nFill in the blank. Ask {other_player} if they have any _____'s? (for ex: type '3' or 'Ace') ")
        if card_ask == "hand":
            self.show_player_hand(current_player)
            self.player_turn(current_player, other_player)
        elif self.check_player_hand(other_player, card_ask):
            #call the go_fish(other_player, card_ask) method which will remove any card with this number from other_player's hand
            #add the card to current_player's hand and call a function to "put down the pair" (removing both cards from current_player's hand)
            #re-call the player_turn(current_player, other_player) method
            print("...hands over card...")
        else:
            #call the draw_card() function and add the card to player1_hand
            print(f"Go Fish! Drawing a card from the deck.\nNow it's {other_player}'s turn.")
            #
            self.player_turn(other_player,current_player)

    def go_fish(self, player, card_val):
        #run through player's hand and check for a card with the same card_val.string_val
        #return True or False
        return self

    def check_player_hand(self, player, card):
        #return True or False
        return True

    def show_player_hand(self, player):
        #display the player_hand list based on which player was passed in
        print("-------- This is your hand -----------")
        if player == self.player1:
            for card in self.player1_hand:
                print(f"{card.string_val} of {card.suit}")
        return self