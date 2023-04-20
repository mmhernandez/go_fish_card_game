from flask_app.models import card

class Deck:
    def __init__(self):
        self.suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        self.cards = []

        for suit in self.suits:
            for i in range(1, 14):
                
                face_value = ""
                if i == 1:
                    face_value == "Ace"
                elif i == 11:
                    face_value == "Jack"
                elif i == 12:
                    face_value == "Queen"
                elif i == 13:
                    face_value == "King"
                else:
                    face_value = str(i)
                self.cards.append(card.Card(suit, face_value, i))

