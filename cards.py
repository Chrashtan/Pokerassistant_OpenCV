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

class CardProperties:
    """Structure to store information about the cards of the camera image."""

    def __init__(self):
        self.frame = []  # Frame of card
        self.corner = []  # Corner of card
        self.width = 0  # Width of card
        self.height = 0  # height of card
        self.rank_img = []  # Image of card's rank
        self.suit_img = []  # Image of card's suit
        CardRanks.rank_name = 0  # Name of the rank of the card. Has to be determined
        CardSuits.suit_name = 0  # Name of the suit of the card. Has to be determined


class CardRanks(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class CardSuits(Enum):
    DIAMONDS = 1
    CLUBS = 2
    HEARTS = 3
    SPADES = 4
