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

DEBUG = False       # FLAG to control whether some code runs or not....for testing

suits = {"Hearts":'♥',
         "Clubs": '♣',
         "Diamonds":'♦',
         "Spades":'♠'}

lost = False        # Game ends when any player reaches the losing total
deal_number = 0     # Which deal this is (1,2,3... so we know how to pass cards)
losing_total = 100  # Play until someone gets this total
points = [0,0,0,0]  # Points for each player

hands = []          # Holds each player's hand of cards
tricks = [[],[],[],[]]         # Holds each player's won tricks
scores = [0,0,0,0]  # Total score of each player. Will update after each deal
curr_trick = []     # Temporarily holds the current trick until it is over. Then move to tricks[]
pass_cards = []     # Holds each player's cards being passed
broken = False      # keep track of whether hearts have been broken in the current deal or not.

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
    # Start by clearing all hands
    global hands
    hands = [[],[],[],[]]

    # Pick a random card, and give it to each person in turn
    for i in range(13):
        for p in range(4):
            card = random.choice(deck)
            deck, hands[p] = move_cards(deck, [card], hands[p])

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
    to_hand += (cards_to_move)
    from_hand = remove_cards(from_hand, cards_to_move)

    return from_hand, to_hand

# Removes the specified cards from the specified hand
# INPUTS:
#   from_hand   - hand from which cards will be removed
#   cards       - list of cards to be removed
#
# ASSUMPTIONS:
#   list of cards is already validated that they exist in the from_hand
def remove_cards(from_hand, cards):
    for card in cards:
        try:
            from_hand.remove(card)
        except:
            # if it isn't in the hand, just move to next card
            pass

    return from_hand    # so calling function can make use of it

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
    str = " ".join(hands[player_num])

    print("")
    print(player_name + ", your hand currently contains the following cards:")
    print(str)

# Prints the specified player's hand
def print_current_trick():
    print("\nThe following cards have been played in this trick so far:")
    print(" ".join(curr_trick))



#</editor-fold>

#<editor-fold desc="Validation Functinos">
# --------------------------------------------------------
# Validation Functions
# --------------------------------------------------------

# Check if exactly the correct number of cards is being passed
# INPUTS:
#   passed_cards - a list of cards being passed
#   expected_value - the number of cards that should be passed (usually 3)
# RETURNS:
#   True / False
def passed_three_cards(passed_cards, expected_value):
    if len(passed_cards) == expected_value:
        return True
    else:
        return False

# Checks if the specified card is in list
# INPUTS:
#   card - the card being checked
#   hand - the list that may contain the card
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
        if card[1] != suits[suit_name]:
            return False

    return True

# Checks if this is the first card in the trick (so it defines the lead suit)
def is_lead(curr_trick):
    if len(curr_trick) == 0:
        return True
    else:
        return False

# Checks if a card is a point card (all Hearts and Q of Spades)
def is_point_card(card):
    if card[1] == suits["Hearts"] or card == "Q"+suits["Spades"]:
        is_point_card = True
    else:
        is_point_card = False

# Checks if the specified card follows the lead suit.
# NOTES:
#   If this is the first card in the trick, then the answer will always be yes
def follows_lead(card, curr_trick):
    ret_val = False

    if is_lead(curr_trick):
        ret_val = True
    else:
        if card[-1] == curr_trick[0][-1]:
            ret_val = True
        else:
            ret_val =  False

    return ret_val


# Checks if the player has any cards in the specified suit
# INPUTS:
#   player_num  - the number of the player whose hand should be checked
#   suit        - the symbol of the suit to be checked
def has_any_in_suit(player_num, suit):
    has_some = False
    for card in hands[player_num]:
        if card[1] == suit:
            has_some = True

    return has_some

# Checks if the specified card is a heart
def is_heart(check_card):
    if check_card[-1] == suits["Hearts"]:
        return True
    else:
        return False

# Calculates the point value of the specified card
def point_value(check_card):
    if is_heart(check_card) == True:
        return 1
    elif check_card[0] == 'Q' and check_card[-1] == suits["Spades"]:
        return 13
    else:
        return 0

    return 0

# Checks if the player has any other suit than the card the specified card's suit
def has_any_other_suit(player_num, card):
    has_some = False
    for card in hands[player_num]:
        if hands[1] != card[1]:
            has_some = True
    return has_some

# Gets the lead suit. If it is blank it means it is not set yet
def current_lead(curr_trick):
    if len(curr_trick) > 0:
        lead_suit = curr_trick[0][1]
    else:
        lead_suit = ''


# Determines if the specified player is allowed to play the specified point card
def can_play_point_card(palyer_num, card):
    if is_heart(card) == True:
        if broken == True:
            return True
        else:
            if has_any_other_suit(curr_player, card) == True:
                print("Hearts have not been broken yet and you have other choices. Must play one of those first.")
                return False
            else:
                return True
    else:
        return True


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

# Checks that card is a valid card to play.
#
# NOTES:
#   There are many requirements about how to validate a card. It depends upon which trick is current, if the player is the
#   lead player, if hearts have been broken, if the card is worth points and if they user has various alternate choices
#   Logic is complex and detailed in a flow chart in the project directory
#
# ASSUMPTIONS:
#   the card being played is assumed to be in the player's hand.
def card_valid_to_play(player_num, card, trick_number):
    # If this is the first card in the first trick of the deal, then it must be a 2Club
    if trick_number == 0 and is_lead(curr_trick):
        if card != "2" + suits["Clubs"]:
            print("First card in a new deal must be a 2 of Clubs.")
            return False
        else:
            return True

    if is_lead(curr_trick):
        # This card is the lead card
        if is_point_card(card) == True:
            return can_play_point_card(curr_player, card)
        else:
            return True
    else:
        # This card is not the lead card in the trick
        if follows_lead(card, curr_trick) == True:
            return True
        else:
            if has_any_in_suit(player_num, curr_trick[0][1]) == True:
                print("You must follow suit if you can.")
                return False
            else:
                # Check if points can be played
                if is_point_card(card) == True:
                    return can_play_point_card(curr_player, card)
                else:
                    return True

    # It should never get to here, but just in case, print an error message and return false
    print("Error validating card")
    return False


# Returns list of cards the user has elected to pass
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

# Asks the player for a single card from their hand.
# Validates that it is actually in their hand before returning it.
# If it isn't, just keeps asking until it is.
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

# Returns the numeric value of the card
def get_card_value(card):
    if card[:-1].lower() == 'a':
        val = 14
    elif card[:-1].lower() == 'k':
        val = 13
    elif card[:-1].lower() == 'q':
        val = 12
    elif card[:-1].lower() == 'j':
        val = 11
    else:
        val = card[:-1]

    return int(val)


# Returns the index of the winning card in the trick
def find_winning_card(trick):
    # First card is lead suit, find the winning card in the trick
    curr_winner = 0
    max_in_lead_suit = 0

    for index, card in enumerate(trick):
        if index == 0:
            lead_suit = card[-1]
            max_in_lead_suit = get_card_value(card)
            curr_winner = 0
        elif card[-1] == lead_suit and get_card_value(card) > max_in_lead_suit:
            # check if it is bigger than any previous card in lead suit....if so, it is current winner
            max_in_lead_suit = get_card_value(card)
            curr_winner = index
        else:
            # not trump suit, so can't win
            pass

    return curr_winner

#</editor-fold>






# Counts points in the trick and adds them to the score totals for each player
def  add_to_total_scores(curr_trick, lead_player):
    pass





# ---------------- BEGIN PROGRAM -----------------------
# Continue dealing new cards until someone loses.
while lost == False:
    broken = False      # Track whether or not Hearts have been broken in this deal yet

    if DEBUG:
        deal_number = 3

    begin_deal(deal_number)

    # Cards have now been dealt, passed and we are ready to play!

    # Each Deal should take exactly 13 tricks to play.
    for trick in range(13):
        curr_trick = []
        print("\n\n")
        print("Begin Trick #", trick)

        # If this is the first trick in the deal, then the player who has 2Clubs must start
        if trick == 0:
            # find 2 of clubs...make this person the start person
            lead_player  = find_two_clubs()

        # Need to remember who started the trick
        curr_player = lead_player

        # Ask all four players to play a card. Start with current player
        for i in range(4):
            valid_card = False

            # Keep asking the player until they give a valid card to play.
            while not valid_card:
                print("")
                # Gets a card out of player's hand
                if DEBUG:
                    # Find the first valid card to play.
                    for card in hands[curr_player]:
                        if card_valid_to_play(curr_player, card, trick) == True:
                            valid_card = True
                            curr_trick.append ( card)
                            hands[curr_player].remove(card)
                            break

                else:
                    card = get_card(curr_player, "Player " + str(curr_player))

                    # Check if it is ok to play the card. If so, play it, if not ask for a different card
                    if card_valid_to_play(curr_player, card, trick) == True:
                        valid_card = True
                        curr_trick.append(card)
                    else:
                        # was not valid, so put it back in their hand and ask again
                        hands[curr_player].append(card)

            print_current_trick()
            curr_player = next_player(curr_player)

        # Trick over so add it to the winning player's tricks and make them the new lead player
        new_lead =  ( lead_player + find_winning_card(curr_trick) ) % 4
        lead_player = new_lead
        tricks[lead_player].extend(curr_trick)
        curr_trick = []

    # All 13 tricks have been played, so total scores, and output standings
    for player_num, trick in enumerate(tricks):
        new_points = 0
        for card in trick:
            new_points += point_value(card)

        # If this player didn't shoot the moon, add points to their hand
        if new_points != 26:
            scores[player_num] += new_points
        else:
            # Add to everyone else's hand and exit
            print("Player " + str(player_num) + " shot the Moon!!!!")
            for i in range(4):
                if i != player_num:
                    scores[ i ] += 26

    # Print the scores
    for index, score in enumerate(scores):
        print("Player " + str(index) + ": " + str(score))

    # Check if game is over.
    for score in scores:
        if score >= losing_total:
            lost = True
            break

    deal_number += 1

print("Game is Over!")
