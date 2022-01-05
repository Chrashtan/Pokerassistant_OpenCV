# ***********************************************
# ***********************************************
# **************** Cards function ***************
# ***********************************************
# ***********************************************

# Import libraries
import cv2 as cv
import numpy as np
from enum import Enum


# Properties of the card

class CardRanks(Enum):
    ACE = "Ace"
    TWO = "Two"
    THREE = "Three"
    FOUR = "Four"
    FIVE = "Five"
    SIX = "Six"
    SEVEN = "Seven"
    EIGHT = "Eight"
    NINE = "Nine"
    TEN = "Ten"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"


class CardSuits(Enum):
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    HEARTS = "Hearts"
    SPADES = "Spades"


class CardProperties:
    """Structure to store information about the cards of the camera image."""

    # Constructor of CardProperties
    def __init__(self):
        self.img = []   # Image of the full card
        self.rank_img = []  # Image of card's rank
        self.rank_match = []    # Image of  best match
        self.suit_img = []  # Image of card's suit
        self.suit_match = []    # Image of best match
        self.centerpoint_X = 0
        self.centerpoint_Y = 0
        CardRanks.rank_name = "Unknown"  # Name of the rank of the card. Has to be determined
        CardSuits.suit_name = "Unknown"  # Name of the suit of the card. Has to be determined

    # Constructor of CardProperties
    def __init__(self, img, rank, suit):
        self.img = img   # Image of the full card
        self.rank_img = rank     # Image of card's rank
        self.rank_match = []    # Image of  best match
        self.suit_img = suit  # Image of card's suit
        self.suit_match = []    # Image of best match
        self.centerpoint_X = 0
        self.centerpoint_Y = 0
        CardRanks.rank_name = "Unknown"  # Name of the rank of the card. Has to be determined
        CardSuits.suit_name = "Unknown"  # Name of the suit of the card. Has to be determined

