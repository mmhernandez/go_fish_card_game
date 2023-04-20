from classes.go_fish import Go_Fish

# Use the starter code to make a simple card game of your choice.
# Implement the rules of the card game.
# Make players to interact with the cards.
# Ninja Bonus: Use Inheritance, Class Methods, and Static Methods within your code.

game = Go_Fish("Melissa", "Bradon") 
game.start_game()  


#Go-Fish game
#RULES:
# Two players
# Each player is dealt cards to start the game (a 10-caed hand)
# The goal of the game is to create pairs of each card
# The game ends when a player no longer has any cards

#GAME PLAY
# Player 1 starts by asking if player 2 has a specific card (to create a pair in their own hand)
#   If player 2 does not have the card, they say "Go Fish" and player 1 has to draw from the remainder of the deck
#   If player 2 has the card in their hand, they give the card to player 1
