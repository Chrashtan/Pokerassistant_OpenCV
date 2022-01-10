# ***********************************************
# ***********************************************
# **************** Cards function ***************
# ***********************************************
# ***********************************************

# Import libraries
import cv2 as cv
import numpy as np

# List for Ranks and Suits to get the Cards
RANK_REFS = ["Ace", "King", "Queen", "Jack", "Ten", "Nine", "Eight", "Seven", "Six", "Five", "Four", "Three", "Two"]
SUIT_REFS = ["Spades", "Clubs", "Hearts", "Diamonds"]

# Dictionary to convert the values for the odd calculation
RANK_VAL_DIC = {"Two": "2", "Three": "3", "Four": "4", "Five": "5", "Six": "6", "Seven": "7", "Eight": "8",
                "Nine": "9", "Ten": "T", "Jack": "J", "Queen": "Q", "King": "K", "Ace": "A"}

SUIT_VAL_DIC = {"Spades": "s", "Clubs": "c", "Hearts": "h", "Diamonds": "d"}


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
        self.rank_name = "Unknown"  # Name of the rank of the card. Has to be determined
        self.suit_name = "Unknown"  # Name of the suit of the card. Has to be determined
        self.card_name = " "    # Value of the Card for Odds
        self.cycle_age = 0  # cycles since the card has been last recognized
        self.contour = []

    def __init__(self, img = [], img_rank = [], img_suit = [], cX = 0, cY = 0, rank = "Unknown", suit = "Unknown"):
        self.img = img   # Image of the full card
        self.rank_img = img_rank     # Image of card's rank
        self.rank_match = []    # Image of  best match
        self.suit_img = img_suit  # Image of card's suit
        self.suit_match = []    # Image of best match
        self.centerpoint_X = cX
        self.centerpoint_Y = cY
        self.rank_name = rank  # Name of the rank of the card. Has to be determined
        self.suit_name = suit  # Name of the suit of the card. Has to be determined
        self.card_name = convertCardName(rank, suit)  # Value of the Card for Odds
        self.cycle_age = 0  # cycles since the card has been last recognized
        self.contour = []


def convertCardName(rank, suit):
    """Gets the Rank and the suit of one card and merge them together"""
    return RANK_VAL_DIC[rank] + SUIT_VAL_DIC[suit]






