# This program 'deals' 5 cards using the Deck of Cards API 
# First it shuffles the deck, then it prints out the 5 cards,
# Finally it congratulates the user if they draw a pair, triple, 
# or straight or all of the same suit
# Authored by: Stephen Kerr

# Imports
import requests

def deal_a_card(number_of_cards):
    # check the input is a positive integer
    if not isinstance(number_of_cards, int) or number_of_cards < 1:
        raise ValueError("number_of_cards must be a positive integer")
    # shuffle a new deck and get deck_id
    url = 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    deck_id = data.get('deck_id')
    if not deck_id:
        raise RuntimeError("Could not obtain deck_id from API response")
    # draw the requested number of cards in one request
    draw_resp = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={number_of_cards}", timeout=10)
    draw_resp.raise_for_status()
    draw_data = draw_resp.json()
    cards = draw_data.get('cards')
    if not cards:
        raise RuntimeError("No cards returned from draw request")
    for c in cards:
        print(f"{c.get('value')} of {c.get('suit')}")
    return cards

if __name__ == "__main__":
    deal_a_card(1)