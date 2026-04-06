# This program 'deals' 5 cards using the Deck of Cards API 
# First it shuffles the deck, then it prints out the 5 cards,
# Finally it congratulates the user if they draw a pair, triple, 
# or straight or all of the same suit
# See API website here: https://deckofcardsapi.com/
# Authored by: Stephen Kerr

# Imports
import requests

# add a value map for the face cards to
value_map = {
    'ACE': 14,
    'KING': 13,
    'QUEEN': 12,
    'JACK': 11,
    '10': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}


def is_straight(numeric_ranks, hand_size):
    uniq = sorted(set(numeric_ranks))
    if len(uniq) != hand_size:
        return False
    if max(uniq) - min(uniq) == hand_size - 1:
        return True
    # Ace-low straight (A,2,3,4,5)
    if 14 in uniq:
        ace_low = sorted(set([1 if r == 14 else r for r in numeric_ranks]))
        return len(ace_low) == hand_size and max(ace_low) - min(ace_low) == hand_size - 1
    return False


def deal_cards(number_of_cards):
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
    draw_response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={number_of_cards}", timeout=10)
    draw_response.raise_for_status()
    draw_data = draw_response.json()
    cards = draw_data.get('cards')
    if not cards:
        raise RuntimeError("No cards returned from draw request")
    
    # track suits 
    suits = []
    # track values
    values = []
    # numeric values for the cards
    numeric_values = []

    for c in cards:
        suits.append(c.get('suit')) # add the suit to the list of suits
        values.append(c.get('value')) # add the value to the list of values
        numeric_values.append(value_map.get(c.get('value')))
        print(f"{c.get('value')} of {c.get('suit')}")

    # evaluate the hand
    is_flush = len(set(suits)) == 1
    straight = is_straight(numeric_values, number_of_cards)
    value_counts = sorted((values.count(v) for v in set(values)), reverse=True)

    if is_flush and straight:
        print("Congratulations! Straight flush!")
    elif is_flush:
        print("Congratulations! Flush — all the same suit!")
    elif straight:
        print("Congratulations! Straight!")
    elif value_counts[0] == 4:
        print("Congratulations! Four of a kind!")
    elif value_counts[0] == 3 and value_counts[1] == 2:
        print("Congratulations! Full house!")
    elif value_counts[0] == 3:
        print("Congratulations! Three of a kind!")
    elif value_counts[0] == 2 and value_counts[1] == 2:
        print("Congratulations! Two pair!")
    elif value_counts[0] == 2:
        print("Congratulations! One pair!")
    else:
        print("Sorry, you didn't draw any pairs or flushes this time. Better luck next time!")

    

    return cards

if __name__ == "__main__":
    deal_cards(5)