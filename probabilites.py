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

board = ["Qc", "Th", "8s"] # Flop: the first three cards on the board
#board = ["Ac","Kc","Qc"]
villan_hand = None #This is an object of the type Combo (part of Poker.Hand). None if no prior knowledge is known about the villan
exact_calculation = True # True = exact calculation; False = Monte Carlo simulation
verbose = True #This is a boolean which is True if you want Holdem Calculator to return the odds of the villan making a certain poker hand, e.g., quads, set, straight. It only supports heads-up scenario.
num_sims = 1 #number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
read_from_file = None

# My hand
hero_hand = Combo('KsJc') # our own hand
#hero_hand = Combo('JcTc') # our own hand

# reveals flop
flop = board
odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                        num_sims, read_from_file ,
                        hero_hand, villan_hand,
                        verbose, print_elapsed_time = False)

hero_odds.append(odds[0]['win'])
print("My probabilities after the FLOP:")
print(odds[0])
print("The probabilities of the poker hands:")
print(odds[1])
print("")

# reveals turn
turn = ["9h"]
board = flop + turn

villan_hand = None

odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                            num_sims, read_from_file ,
                            hero_hand, villan_hand,
                            verbose, print_elapsed_time = False)
hero_odds.append(odds[0]['win'])
print("My probabilities after the TURN:")
print(odds[0])
print("The probabilities of the poker hands:")
print(odds[1])
print("")

# reveals river
river = ["Kh"]
board = flop + turn + river
verbose = True

villan_hand = None

odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                            num_sims, read_from_file ,
                            hero_hand, villan_hand,
                            verbose, print_elapsed_time = False)
hero_odds.append(odds[0]['win'])

print("My probabilities after the RIVER:")
print(odds[0])
print("The probabilities of the poker hands:")
print(odds[1])
print("")


# Determine Winner
verbose = True

villan_hand = Combo('3h4h')

odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                            num_sims, read_from_file ,
                            hero_hand, villan_hand,
                            verbose, print_elapsed_time = False)

print("Determine the winner (aus meiner Sicht):")
print(odds[0])
print("")
print("After River (odds[1]:", odds[1])

if(percentages[1]==1):
    print("Player 1 has won")
else:
    print("Player 2 has won")


