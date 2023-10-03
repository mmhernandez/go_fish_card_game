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
            "deck": remaining_deck
        }
        return game_dict
    

    @staticmethod
    def check_for_pairs(hand):
        flag = False
        lookup_dict = {}
        for i in range(len(hand)):
            # determine if any pairs are present in the hand
            if hand[i]["point_value"] in lookup_dict:
                # set flag to True if pair exists and break out of loop
                flag = True
                break   
            else:
                lookup_dict[hand[i]["point_value"]] = i
        return flag

    @staticmethod
    def check_for_computer_pairs(hand):
        hasPairs = False
        pairs = []
        lookup_dict = {}
        for i in range(len(hand)):
            if hand[i]["point_value"] in lookup_dict:
                first_pair_card = hand[lookup_dict[hand[i]["point_value"]]]
                pairs.append(first_pair_card)

                current_pair_card = hand[i]
                pairs.append(current_pair_card)

                hasPairs = True
                break
            else:
                lookup_dict[hand[i]["point_value"]] = i

        result_dict = {
            "hasPairs": hasPairs,
            "pairs_list": pairs
        }

        return result_dict

    @staticmethod
    def lay_down_pairs_computer(hand, deck):
        pairs = []
        lookup_dict = {}
        for i in range(len(hand)):
            if hand[i]["point_value"] in lookup_dict:
                first_pair_card = hand[lookup_dict[hand[i]["point_value"]]]
                pairs.append(first_pair_card)

                current_pair_card = hand[i]
                pairs.append(current_pair_card)
                
                del lookup_dict[first_pair_card["point_value"]]

            else:
                lookup_dict[hand[i]["point_value"]] = i

        new_hand = []
        for value in lookup_dict.values():
            new_hand.append(hand[value])

        updated_game_dict = {
            "hand": new_hand,
            "pairs": pairs,
            "deck": deck
        }

        #call method to draw from the deck
        if len(pairs) > 0:
            updated_cards = Game.draw_from_deck(new_hand, deck)
            updated_game_dict["hand"]: updated_cards["hand"]
            updated_game_dict["deck"]: updated_cards["deck"]
        
        return updated_game_dict
    

    @staticmethod
    def lay_down_pairs(hand, pair_list, deck):
        new_pair = []        
        # add pairs to the new_pairs list
        new_pair.append(pair_list[0])
        new_pair.append(pair_list[1])

        # remove paired cards from hand
        #   create list of indexes that do not include the pair cards
        index_list = []
        for i in range(len(hand)):
            for j in range(len(pair_list)):
                if hand[i]["suit"] == pair_list[j]["suit"] and hand[i]["face_value"] == pair_list[j]["face_value"]:
                    index_list.append(i)
        #   add cards from index list to a new hand (which doesn't include pair cardss)
        new_hand = []
        for i in range(len(hand)):
            if i not in index_list:
                new_hand.append(hand[i])

        updated_game_dict = {
            "hand": new_hand,
            "pairs": new_pair,
            "deck": deck
        }

        return updated_game_dict


    @staticmethod
    def draw_from_deck(hand, deck):
        while len(hand) < 7:
            rand_card = random.choice(deck)
            rand_card_index = deck.index(rand_card)
            deck.pop(rand_card_index)
            hand.append(rand_card)

        updated_cards = {
            "hand": hand,
            "deck": deck
        }
        return updated_cards


    @staticmethod
    def check_hand_for_card(request_hand, check_hand, point_value, deck):
        flag = False
        for i in range(len(check_hand)):
            if flag == True:
                break
            if check_hand[i]["point_value"] == point_value:
                card_to_transfer = check_hand.pop(i)
                request_hand.append(card_to_transfer)
                flag = True

        result_game_dict = {
            "request_hand": request_hand,
            "check_hand": check_hand,
            "deck": deck,
            "flag": flag
        }

        if flag == True:
            updated_check_hand_dict = Game.draw_from_deck(result_game_dict["check_hand"], result_game_dict["deck"])
            result_game_dict["check_hand"] = updated_check_hand_dict["hand"]
            result_game_dict["deck"] = updated_check_hand_dict["deck"]

        return result_game_dict
    

    @staticmethod
    def computer_turn(computer_hand, player_hand, deck):
        flag = True
        while (flag == True):
            # loop through computer hand to determine if there are any pairs
            # pairs = []
            # lookup_dict = {}
            # for i in range(len(computer_hand)):
            #     if computer_hand[i]["point_value"] in lookup_dict:
            #         first_pair_card = computer_hand[lookup_dict[computer_hand[i]["point_value"]]]
            #         pairs.append(first_pair_card)

            #         current_pair_card = computer_hand[i]
            #         pairs.append(current_pair_card)
                    
            #         del lookup_dict[first_pair_card["point_value"]]
            #         break
            #     else:
            #         lookup_dict[computer_hand[i]["point_value"]] = i
            

            #check for pairs in computer hand
            pairs_check_dict = Game.check_for_computer_pairs(computer_hand)
            # if there are pairs, lay them down
            if(pairs_check_dict["hasPairs"]):
                updated_cards_dict = Game.lay_down_pairs(computer_hand, pairs_check_dict["pairs_list"], deck)

                computer_hand = updated_cards_dict["hand"]
                computer_pairs = updated_cards_dict["pairs"]
                deck = updated_cards_dict["deck"]

            # if no pairs, check player hand for possible pair
            else:
                # pick random card in computer's hand
                rand = random.randint(0,len(computer_hand))
                rand_point_value = computer_hand[rand]

                print(f'rand = {rand}')
                print(f'rand_point_value = {rand_point_value}')

                # check if a match is available in the player hand
                result = Game.check_hand_for_card(computer_hand, player_hand, rand_point_value)
                # if match found, take card from player, lay down pairs, and draw from deck
                if result["flag"]:
                    pass
                #   if no match found, set flag to false to end computer turn
                else:
                    flag = False

        

        result_game_dict = {
            "computer_hand": computer_hand,
            "computer_pairs": computer_pairs,
            "player_hand": player_hand,
            "deck": deck
        }

        return result_game_dict

