# This program 'deals' 5 cards using the Deck of Cards API 
# First it shuffles the deck, then it prints out the 5 cards,
# Finally it congratulates the user if they draw a pair, triple, 
# or straight or all of the same suit
# Authored by: Stephen Kerr

# Imports
import requests

# setting up the url and get() request
url = 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
response = requests.get(url)
data = response.json()


print(data)