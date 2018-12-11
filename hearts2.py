
import random

'''
Get a list of keys from dictionary which has the given value
'''
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys



# Represents a standard playing Card
class Card(object):
    # Name of suits and their symbol
    suits = {'Clubs': '♣',
             'Diamonds': '♦',
             'Spades': '♠',
             'Hearts': '♥',
             }

    # List of ranks. Note that the "value" is the index of the rank
    ranks = ( None, None, 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A" )


    def __init__(self, rank = 2, suit = 0):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        # Ensure that each card takes up 3 spaces so it lines up nicely when printed
        str = '%s' % (self.rank)
        if len(str)<2:
            str = " " + str
        str = str + Card.suits[self.suit]
        return str

    # Compare two cards to see if card is less than other....first by suit, then by value
    def __lt__(self, other):
        t1 = self.suit, self.value()
        t2 = other.suit, other.value()
        return t1 < t2

    # Compare two cards to see if card is greater than other....first by suit, then by value
    def __gt__(self, other):
        t1 = self.suit, self.value()
        t2 = other.suit, other.value()
        return t1 > t2

    # Compare two cards to see if card is equal to other....first by suit, then by value
    def __eq__(self, other):
        t1 = self.suit, self.value()
        t2 = other.suit, other.value()
        return t1 == t2



    def value(self):
        return Card.ranks.index(self.rank)

    def point_value(self):
        if self.suit == 'Hearts':
            return 1
        elif self.suit == 'Spades' and self.rank == 'Q':
            return 13
        else:
            return 0

class Deck(object):
    """represents a deck of cards"""

    def __init__(self):
        self.cards = []
        for suit in Card.suits:
            for rank in range(2,15):
                card = Card(Card.ranks[rank], suit)
                self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return ', '.join(res)

    def add_card(self, card):
        """add a card to the deck"""
        self.cards.append(card)

    def pop_card(self, i=-1):
        """remove and return a card from the deck.
        By default, pop the last card."""
        return self.cards.pop(i)

    def pop_cards(self, num_cards):
        popped = []
        if num_cards > len(self.cards):
            return popped
        else:
            for i in range(num_cards):
                popped.append( self.pop_card())

        return popped

    def shuffle(self):
        """shuffle the cards in this deck"""
        random.shuffle(self.cards)

    def sort(self):
        """sort the cards in ascending order"""
        self.cards.sort()

    def move_cards(self, hand, num):
        """move the given number of cards from the deck into the Hand"""
        for i in range(num):
            hand.add_card(self.pop_card())


class Hand(Deck):
    """represents a hand of playing cards"""

    def __init__(self, label=''):
        self.label = label
        self.cards = []

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return ', '.join(res)

    def display_hand(self):
        print( self.label + "'s hand: " + str(self))


class Trick(object):
    def __init__(self, lead_player = 0):
        self.lead_player = lead_player
        self.cards = []

    # Calculate the total points in this trick
    def total_points(self):
        pts = 0
        for card in self.cards:
            pts += card.point_value()

        return pts

    # Determine which player won the trick.
    # Example:  If player 2 was the lead player, then their card is the first in the trick
    #           and it is the lead suit. So figure out which card is the greatest....and then return the payer index of the winning player
    def winning_player_number(self):
        # First card is lead suit, find the winning card in the trick
        winning_card_index = 0
        trump_suit = self.cards[0].suit
        curr_max_value = 0

        for index, card in enumerate(self.cards):
            if index == 0:
                curr_max_value = card.value()
                winning_card_index = 0
            elif card.suit == trump_suit and card.value() > curr_max_value:
                curr_max_value = card.value()
                winning_card_index = index
            else:
                # not lead_suit, so can't win
                pass

        # Now figure out which player is the winner of this trick
        retval =  (self.lead_player + winning_card_index ) % 4
        return retval



