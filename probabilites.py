# ------ Import libaries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import cards
import processVideo
import processVideo as pV
from itertools import combinations

import pandas as pd
import numpy as np
import itertools


from poker import Range
from IPython.core.display import display, HTML

hero_odds = []
hero_range_odds = []

from poker.hand import Combo

import holdem_calc
import holdem_functions

def probabilityFLOP(board, hero_hand, villan_hand):
    """Returns 2 Strings"""
    # Fix constants
    exact_calculation = False  # True = exact calculation; False = Monte Carlo simulation
    verbose = True  # This is a boolean which is True if you want Holdem Calculator to return the odds of the villan making a certain poker hand, e.g., quads, set, straight. It only supports heads-up scenario.
    num_sims = 5  # number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
    read_from_file = None

    odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                        num_sims, read_from_file ,
                        hero_hand, villan_hand,
                        verbose, print_elapsed_time = False)
    OddsString = "Tie: " + str(odds[0]['tie']) + " Win: " + str(odds[0]['win']) + " Lose: " + str(odds[0]['lose'])
    max_value = None
    for num2 in odds[1][0].values():
        if (max_value is None or num2 > max_value):
            max_value = num2
    for key, value in odds[1][0].items():
        if max_value == value:
            handstring = "highest hand probability: " + str(key) + " " + str(round(max_value*100,2)) + "%"

    return OddsString, handstring

def probabilityTURN(board, hero_hand, villan_hand):
    """Returns 2 Strings"""

    # Fix constants
    exact_calculation = False  # True = exact calculation; False = Monte Carlo simulation
    verbose = True  # This is a boolean which is True if you want Holdem Calculator to return the odds of the villan making a certain poker hand, e.g., quads, set, straight. It only supports heads-up scenario.
    num_sims = 5  # number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
    read_from_file = None

    odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                                 num_sims, read_from_file ,
                                 hero_hand, villan_hand,
                                 verbose, print_elapsed_time = False)
    OddsString = "Tie: " +str(odds[0]['tie']) + " Win: " + str(odds[0]['win']) + " Lose: " + str(odds[0]['lose'])
    max_value = None
    for num2 in odds[1][0].values():
        if (max_value is None or num2 > max_value):
            max_value = num2
    for key, value in odds[1][0].items():
        if max_value == value:
            handstring = "highest hand probability: " + str(key) + " " + str(round(max_value*100,2)) + "%"

    return OddsString, handstring

def probabilityRIVER(board, hero_hand, villan_hand):
    """probabilityRIVER"""
    # Fix constants
    exact_calculation = False  # True = exact calculation; False = Monte Carlo simulation
    verbose = True  # This is a boolean which is True if you want Holdem Calculator to return the odds of the villan making a certain poker hand, e.g., quads, set, straight. It only supports heads-up scenario.
    num_sims = 5  # number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
    read_from_file = None

    odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                                 num_sims, read_from_file ,
                                 hero_hand, villan_hand,
                                 verbose, print_elapsed_time = False)
    hero_odds.append(odds[0]['win'])
    OddsString = "Tie: " +str(odds[0]['tie']) + " Win: " + str(odds[0]['win']) + " Lose: " + str(odds[0]['lose'])
    max_value = None
    for num2 in odds[1][0].values():
        if (max_value is None or num2 > max_value):
            max_value = num2
    for key, value in odds[1][0].items():
        if max_value == value:
            handstring = "highest hand probability: " + str(key) + " " + str(round(max_value*100,2)) + "%"

    return OddsString, handstring


def findWINNER(board, hero_hand, villan_hand):
    """Determine the winner"""
    # Fix constants
    exact_calculation = False  # True = exact calculation; False = Monte Carlo simulation
    verbose = True  # This is a boolean which is True if you want Holdem Calculator to return the odds of the villan making a certain poker hand, e.g., quads, set, straight. It only supports heads-up scenario.
    num_sims = 5  # number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
    read_from_file = None

    odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                                 num_sims, read_from_file ,
                                 hero_hand, villan_hand,
                                 verbose, print_elapsed_time = False)
    hero_odds.append(odds[0]['win'])
    if(odds[0]['win']>99):
        return "You win"
    elif(odds[0]["tie"]>49):
        return "Splitt pot"
    else:
        return "You lose"








