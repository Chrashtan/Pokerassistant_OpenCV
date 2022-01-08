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
import keyboard

from poker import Range
from IPython.core.display import display, HTML

hero_odds = []
hero_range_odds = []

from poker.hand import Combo

import holdem_calc
import holdem_functions

def get_key(val):
    for key, value in odds[1][0].items():
        if val == value:
            return key

    return "There is no such Key"

board = ["Qc", "Th", "8s"]  # Flop: the first three cards on the board
#board = ["Ac","Kc","Qc"]
villan_hand = None #This is an object of the type Combo (part of Poker.Hand). None if no prior knowledge is known about the villan
exact_calculation = False # True = exact calculation; False = Monte Carlo simulation
verbose = True #This is a boolean which is True if you want Holdem Calculator to return the odds of the villan making a certain poker hand, e.g., quads, set, straight. It only supports heads-up scenario.
num_sims = 5 #number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True
read_from_file = None

# My hand
hero_hand = Combo('KsJc') # our own hand
#hero_hand = Combo('JcTc') # our own handd


# print("Choose: YES=[y] or NO=[n]")
# input = input('Wurde der FLOP aufgedeckt?: ')
# while True:
#     if keyboard.read_key() == "y":

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
print("WERT", odds[1][0])
first =[]
first.extend(odds[1][0].values())
print(first)

print("")
max_value2 = None
max_value = None

for num2 in odds[1][0].values():
    if (max_value2 is None or num2 > max_value2):
        max_value2 = num2
#for num in odds[1][0]:
#    if (max_value is None or num > max_value):
#        max_value = num

print(get_key(max_value2), max_value2)

print('Highest probability:',max_value, max_value2)
print("")
print("")

def get_key(val):
    for key, value in odds[1][0].items():
        if val == value:
            return key

    return "There is no such Key"
print(get_key(max_value2))





def probabilityFLOP(board, hero_hand, villan_hand, exact_calculation,num_sims, read_from_file, verbose):
    odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                        num_sims, read_from_file ,
                        hero_hand, villan_hand,
                        verbose, print_elapsed_time = False)
    mystring = "Tie"+ odds[0]['tie'] + "Win" + odds[0]['win'] + "Lose" + odds[0]['lose']
    return  mystring

    hero_odds.append(odds[0]['win'])
    print("My probabilities after the FLOP:")
    print(odds[0])
    print("The probabilities of the poker hands:")
    print(odds[1])
    print("")


# ------------- TURN ------------------
# # reveals turn

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
print(odds[1][0])
first =[]
first.extend(odds[1][0].values())
print(first)

print("")
max_value2 = None
max_value = None

for num2 in odds[1][0].values():
    if (max_value2 is None or num2 > max_value2):
        max_value2 = num2
#for num in odds[1][0]:
#    if (max_value is None or num > max_value):
#        max_value = num
#print('Highest probability:',max_value, max_value2)

for key, value in sorted(odds[1][0].items(), key=lambda item: item[1]):
    ("%s: %s" % (key,value))
print("Höhste Karte")
print(get_key(max_value2), max_value2)
print("")
print("")
print(get_key(max_value2), max_value2)






def probabilityTURN(board, hero_hand, villan_hand, exact_calculation,num_sims, read_from_file, verbose):
    odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                                 num_sims, read_from_file ,
                                 hero_hand, villan_hand,
                                 verbose, print_elapsed_time = False)
    mystring = "Tie" + odds[0]['tie'] + "Win" + odds[0]['win'] + "Lose" + odds[0]['lose']
    return mystring

    hero_odds.append(odds[0]['win'])
    print("My probabilities after the TURN:")
    print(odds[0])
    print("The probabilities of the poker hands:")
    print(odds[1])
    print(odds[0]['win'])



# reveals river
river = ["Kh"]
board = flop + turn + river
verbose = True

villan_hand = None

def probabilityRIVER(board, hero_hand, villan_hand, exact_calculation,num_sims, read_from_file, verbose):
    odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                                 num_sims, read_from_file ,
                                 hero_hand, villan_hand,
                                 verbose, print_elapsed_time = False)
    hero_odds.append(odds[0]['win'])
    mystring = "Tie" + odds[0]['tie'] + "Win" + odds[0]['win'] + "Lose" + odds[0]['lose']
    return mystring

    print("My probabilities after the RIVER:")
    print(odds[0])
    print("The probabilities of the poker hands:")
    print(odds[1])
    print("")


# Determine Winner
verbose = True
villan_hand = Combo('3h4h')

def findWINNER(board, hero_hand, villan_hand, exact_calculation,num_sims, read_from_file, verbose):
    odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                                 num_sims, read_from_file ,
                                 hero_hand, villan_hand,
                                 verbose, print_elapsed_time = False)
    hero_odds.append(odds[0]['win'])
    if(odds[0]['win']>99):
        result = "You win"
        return result
    elif(odds[0]["tie"]>49):
        return "Splitt pot"
    else:
        return "You lose"



#holdem_functions.find_winner()


