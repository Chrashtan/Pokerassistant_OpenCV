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
    ACE = "ace"
    TWO = "two"
    THREE = "three"
    FOUR = "four"
    FIVE = "five"
    SIX = "six"
    SEVEN = "seven"
    EIGHT = "eight"
    NINE = "nine"
    TEN = "ten"
    JACK = "jack"
    QUEEN = "queen"
    KING = "king"


class CardSuits(Enum):
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    HEARTS = "hearts"
    SPADES = "spades"


class CardProperties:
    """Structure to store information about the cards of the camera image."""

    def __init__(self):
        self.frame = []  # Frame of card
        self.corner = []  # Corner of card
        self.centerpoint = []   # Centerpoint of Card
        self.width = 0  # Width of card
        self.height = 0  # height of card
        self.rank_img = []  # Image of card's rank
        self.suit_img = []  # Image of card's suit
        CardRanks.rank_name = "Unknown"  # Name of the rank of the card. Has to be determined
        CardSuits.suit_name = "Unknown"  # Name of the suit of the card. Has to be determined

