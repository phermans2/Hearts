''' -----------------------------------------------------------
    HEARTS
        RULES:
            Hearts is a card game in which 4 players compete to get
            the least number of points.
            Each heart is worth 1 point, Queen of Spades is worth 13 points

            Deal the entire deck of cards so each player has 13 cards.
            Deal 1 - pass 3 cards to left
            Deal 2 - pass 3 cards to right
            Deal 3 - pass 3 cards across
            Deal 4 - pass 0 cards
            repeat

            Once cards are dealt and passed, play begins with player who
            has the 2 of clubs. They begin and then each player must play in
            clockwise fashion. They must follow suit if they can, but may only play
            a heart if there is no other option, or hearts have been previously been played.

            Once all 4 players have played a card, the Trick is complete and
            the highest ranking card wins the trick. The player who played that card wins the trick
            and must begin the next trick.  Continue until all 13 tricks have been played.

            Total points, then shuffle and deal again.
            Continue process until game is over (when someone reaches at least 100 points)

        AUTHOR:
            Paul Hermans - 2018

'''

import random

#<editor-fold desc="Variable Definitions">
suits = {"Hearts":'♥',
         "Clubs": '♣',
         "Diamonds":'♦',
         "Spades":'♠'}

lost = False        # Game ends when any player reaches the losing total
deal_number = 0     # Which deal this is (1,2,3... so we know how to pass cards)
losing_total = 100  # Play until someone gets this total
points = [0,0,0,0]  # Points for each player

hands = []          # Holds each player's hand of cards
tricks = []         # Holds each player's won tricks
curr_trick = []     # Temporarily holds the current trick until it is over. Then move to tricks[]
pass_cards = []     # Holds each player's cards being passed

#</editor-fold>

#<editor-fold desc="Move Card Functinos">

# Return a list of ALL cards in the specified suit
def generate_suit(suit_name):
    suit = []
    symbol = suits[suit_name]   # Get the symbol from the dictionary
    for i in range(1,14):
        if i == 1:
            suit.append("A" + symbol)
        elif i == 11:
            suit.append("J" + symbol)
        elif i == 12:
            suit.append("Q" + symbol)
        elif i == 13:
            suit.append("K" + symbol)
        else:
            suit.append(str(i) + symbol)
    return suit

# Deal each player 13 cards
# RETURNS:
#   List of 4 hands
def deal_cards(deck):
    hands = []

    # Pick a random card, and give it to each person in turn
    for i in range(13):
        card = random.choice(deck)
        move_cards(deck, card, hands[0])
        move_cards(deck, card, hands[1])
        move_cards(deck, card, hands[2])
        move_cards(deck, card, hands[3])

    return hands

# Take cards out of from_hand and move them into to_hand
# Inputs:
#   from_hand       - hand from which cards are being taken
#   cards_to_move   - list of cards to be moved
#   to_hand         - hand that will receive the cards
#
# ASSUMPTIONS:
#   cards_to_move are all valid cards to move!
# TODO - fix assumptions
def move_cards(from_hand, cards_to_move, to_hand):
    # Take the cards_to_move and move them.
    to_hand.extend(cards_to_move)
    remove_cards(from_hand, cards_to_move)

# Removes the specified cards from the specified hand
# INPUTS:
#   from_hand   - hand from which cards will be removed
#   cards       - list of cards to be removed
#
# ASSUMPTIONS:
#   list of cards is already validated that they exist in the from_hand
def remove_cards(from_hand, cards):

    for elem in cards:
        try:
            from_hand.remove(elem)
        except:
            # if it isn't in the hand, just move to next card
            pass

#</editor-fold>

#<editor-fold desc="Utility Functinos">

# Removes duplicate entries from a list
# RETURNS:
#   list with only unique values in it
def remove_duplicates(list_w_dups):
    final_list = []
    for elem in list_w_dups:
        if elem not in final_list:
            final_list.append(elem)
    return final_list

# Prints the specified player's hand
def print_hand(player_num, player_name):
    line1 = ""
    line2 = ""
    for index, card in enumerate(hands[player_num]):
        line1 += " " + str(index) + " "
        line2 += card + " "

    print(player_name + ", your hand currently contains the following cards:")
    print(line2)

#</editor-fold>

#<editor-fold desc="Validation Functinos">
# --------------------------------------------------------
# Validation Functions
# --------------------------------------------------------
# TODO - cleanup these validation functions!!!


# Check if exactly the correct number of cards is being passed
# INPUTS:
#   passed_cards - a list of cards being passed
# RETURNS:
#   True / False
def passed_three_cards(passed_cards, expected_value):
    if len(passed_cards) == expected_value:
        return True
    else:
        return False

# Checks if card is in list
def card_in_list(card, hand):
    if card in (hand):
        return True
    else:
        return False

# Checks if the specified hand contains any cards of the specified suit
# INPUTS:
#   hand = the hand being checked
#   suit_name = the name of the suit being looked for ("Hearts", "Diamonds" etc)
# RETURNS:
#   True / False
def has_suit( hand, suit ):
    for card in hand:
        if card[1] == suit:
            return True

    return False

# Checks if the hand contains only the specified Suit
def only_has_suit(hand, suit_name):
    for card in hand:
        if card[1] != suit[suit_name]:
            return False

    return True



# Checks if a card is a point card (all Hearts and Q of Spades)
def is_point_card(card):
    if card[1] == suits["Hearts"] or card == "Q"+suits["Spades"]:
        is_point_card = True
    else:
        is_point_card = False

# Check if hand has only point cards in it
def only_has_point_cards(hand):
    has_non_point_card = False
    for card in hand:
        if card[1] != suits["Hearts"] and card == "Q" + suits["Spades"]:
            return False
    else:
        return True

# TODO - finish these if needed
# must have card in hand to use it
# does player not have a specific suit?
# can only play points at some times


# Validate that number of cards being passed is 3 and the player has the specific cards available to pass
# NOTE:
#   This should be called before cards are removed from player's hand!
def validate_passed_cards(player_num, passed_cards):

    # Assume it is valid unless somethign changes that.
    is_valid = True

    # No cards in passed cards can be duplicates.
    passed_cards = remove_duplicates(passed_cards)

    # Must pass exactly 3 cards
    if not passed_three_cards:
        is_valid = False

    # Verify that the 3 cards passed are actually in the player's hand
    for elem in passed_cards:
        if card_in_list(elem, hands[player_num]) == False:
            is_valid = False

    return is_valid

# Checks that card is a valid card to play
def card_valid_to_play(player_num, card, trick_number):
    is_valid = True

    # Check if the trick has been started, and keep track of what the lead suit is
    if len(curr_trick) > 0:
        lead_suit = curr_trick[0][1]
    else:
        lead_suit = ''

    # Check if points are allowed to be played
    if trick_number == 0:
        points_allowed = False
    elif hearts_broken == True:
        points_allowed = True
    else:
        if only_has_suit("Hearts"):
            points_allowed = True
    if points_allowed == True:
        print("Points are allowed!")
    # Card being played must follow suit of the lead card in the trick.
    # If this is the lead card, any card (subject to rules below) will do.
    # Only exception to this is if you have none of the lead suit to play.
    # Then you are still subject to other rules about playing points etc.
    if len(curr_trick) != 0:
        # This is not the lead card, does it follow suit?
        if card[1] != curr_trick[0][1]:
            # Didn't follow lead suit!
            # If they have any cards that would follow lead suit, must play them!
            if has_suit(hands[player_num], curr_trick[0][1]):
                print("You must follow the lead suit for the trick.")
                return False
    else:
        # This is the lead card
        pass
    # Playing points is not allowed in first round unless:
    #   1) You have only hearts in your hand
    #   2) You have only hearts and Q of Spades in your hand.
    #
    #   In case 2, you must play the Q of Spades first.
    #   Otherwise you have no choice but to play a heart


    # Playing hearts is only allowed if you have no choice,
    #   or they have been "broken"




    # Passed
    return is_valid

# Check if the player's hand has any cards of the specified suit in it
def has_suit(player_num, symbol):
    for card in hands[player_num]:
        if card[1] == symbol:
            return True

    return False


# Returns which cards the user has elected to pass
def get_cards_to_pass(player_num, player_name):
    valid = False

    # Keep asking player until they pass valid cards!
    while not valid:
        print_hand(player_num, player_name)

        # Make a list of the cards to pass
        new_cards = input("Which cards would you like to pass?").split(" ")

        # Validate that appropriate number of cards were passed....and that they have those cards to pass!
        valid = validate_passed_cards(player_num, new_cards)
        if valid == False:
            print("\nYou tried to passed invalid cards!")
            print("Make sure you pass only 3 cards and that they are in your hand.\n")

    # Now that they are passing valid cards, remove them from their hand
    remove_cards(hands[player_num], new_cards)

    # Return the list of cards this player is passing
    return new_cards

# Asks the user for a single card from user's hand.
# Validates that it is actually in their hand before returning it.
def get_card(player_num, player_name):
    done = False

    while not done:
        card = ""

        print_hand(player_num, player_name)
        card = input("Which card would you like to play?")

        if card in hands[player_num]:
            # remove this card from the player's hand and return it
            hands[player_num].remove(card)
            return card
        else:
            print(card + " is not in your hand.")
            print("")

#</editor-fold>

#<editor-fold desc="Game Play Functions">

# --------------------------------------------------------
# Game Play Functions
# --------------------------------------------------------
# begin a new deal by shuffling deck, and passing cards.
# deal_number indicates which number deal this is and will
# affect the way cards are passed.
def begin_deal(deal_number):

    pass_direction = deal_number % 4

    # Generate a deck of cards
    deck = []
    for key in suits:
        deck.extend(generate_suit(key))

    # Randomly give each player a set of 13 cards
    hands = deal_cards(deck)

    if pass_direction == 0:
        # Pass Left
        # P0 gives to P1
        # P1 gives to P2
        # P2 gives to P3
        # P3 gives to P0
        # Get cards to pass from each player
        pass_cards.append(get_cards_to_pass(0, "Player 0"))
        pass_cards.append(get_cards_to_pass(1, "Player 1"))
        pass_cards.append(get_cards_to_pass(2, "Player 2"))
        pass_cards.append(get_cards_to_pass(3, "Player 3"))

        # Recieve new cards that were passed
        hands[1].extend(pass_cards[0])
        hands[2].extend(pass_cards[1])
        hands[3].extend(pass_cards[2])
        hands[0].extend(pass_cards[3])
    if pass_direction == 1:
        # Pass Right
        # P0 to P3
        # P3 to P2
        # P2 to P1
        # P1 to P0
        pass_cards.append(get_cards_to_pass(hands[0], "Player 0"))
        pass_cards.append(get_cards_to_pass(hands[1], "Player 1"))
        pass_cards.append(get_cards_to_pass(hands[2], "Player 2"))
        pass_cards.append(get_cards_to_pass(hands[3], "Player 3"))

        # Recieve new cards that were passed
        hands[3].extend(pass_cards[0])
        hands[0].extend(pass_cards[1])
        hands[1].extend(pass_cards[2])
        hands[2].extend(pass_cards[3])
    if pass_direction == 2:
        # P ass Across
        # P0 to P2
        # P1 to P3
        # P2 to P0
        # P3 to P1
        pass_cards.append(get_cards_to_pass(hands[0], "Player 0"))
        pass_cards.append(get_cards_to_pass(hands[1], "Player 1"))
        pass_cards.append(get_cards_to_pass(hands[2], "Player 2"))
        pass_cards.append(get_cards_to_pass(hands[3], "Player 3"))

        # Recieve new cards that were passed
        hands[2].extend(pass_cards[0])
        hands[3].extend(pass_cards[1])
        hands[0].extend(pass_cards[2])
        hands[1].extend(pass_cards[3])
    if pass_direction == 3:
        # Don't pass any cards
        pass

# Returns the next player in the rotation
# Example:
#   player_num = 0, returns 1
#   player_num = 3, returns 0
def next_player(player_num):
    return (player_num+1) % 4

# Returns the number of the player who has the 2 of clubs in their hand
def find_two_clubs():
    for index, hand in enumerate(hands):
        if '2♣' in hand:
            return index

    # This should never happen as somebody must have the 2 of clubs
    return -1

#</editor-fold>

# ---------------- BEGIN PROGRAM -----------------------
while lost == False:
    hearts_broken = False   # Track whether or not Hearts have been broken in this deal yet

    begin_deal(deal_number)

    # Cards have now been dealt, passed and we are ready to play!

    # Each Deal should take 13 tricks to play.
    for trick in range(14):
        curr_trick = []
        print("\n\n")

        if trick == 0:
            # find 2 of clubs...make this person the start person
            curr_player = find_two_clubs()
            pass
        else:
            # make the person who won the last trick the start person
            pass

        # Ask all four players to play a card. Start with current player
        for i in range(4):
            valid_card = False
            while not valid_card:
                # Gets a card out of player's hand
                card = get_card(curr_player, "Player " + str(curr_player))
                if card_valid_to_play(curr_player, card, trick) == True:
                    curr_trick.append(card)
                else:
                    # If the card they played was invalid, put it back in their hand
                    # and ask again until they play a valid card.
                    hands[curr_player].append(card)

            print("Cards Played: ")
            print(curr_trick)
            curr_player = next_player(curr_player)

        # validate that it is a legal move
        # Ask next player, validate
        # Ask next player, validate
        # Ask next player, validate
        # Determine who won trick, add it to their tricks collection
        # Trick over - calculate and report scores


    deal_number += 1
