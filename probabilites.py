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
    num_sims = 10  # number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
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
    num_sims = 10  # number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
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
    num_sims = 10  # number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
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
    num_sims = 10  # number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
    read_from_file = None

    odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                                 num_sims, read_from_file ,
                                 hero_hand, villan_hand,
                                 verbose, print_elapsed_time = False)
    # Calculate Hand for Hero
    max_valueH = None
    for num in odds[1][0].values():
        if (max_valueH is None or num > max_valueH):
            max_valueH = num
    for key, value in odds[1][0].items():
        if max_valueH == value:
            HeroHand = "Hero Hand: " + str(key) + " " + str(round(max_valueH * 100, 2)) + "%"

    # Calculate Hand for Villan
    max_valueV = None
    for num in odds[1][1].values():
        if (max_valueV is None or num > max_valueV):
            max_valueV = num
    for key, value in odds[1][1].items():
        if max_valueV == value:
            VillanHand = "Villan Hand: " + str(key) + " " + str(round(max_valueV * 100, 2)) + "%"

    if(odds[0]['win']>99):
        return "Hero wins", HeroHand, VillanHand
    elif(odds[0]["tie"]>49):
        return "Tie", OddsString, HeroHand, VillanHand
    else:
        return "Villan wins", HeroHand, VillanHand








