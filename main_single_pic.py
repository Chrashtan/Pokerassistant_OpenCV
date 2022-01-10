# ***********************************************
# ***********************************************
# **************** Main script ******************
# ***********************************************
# ***********************************************

# ------ Import libaries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import cards
from poker.hand import Combo
import processVideo as pV
import probabilites as odd

# Constants
CARD_MIN_AREA = 59243
CARD_MAX_AREA = 72409


RESIZE_FACTOR = 1

COLOR_GREEN = (69, 200, 43)
COLOR_BLUE = (255, 0, 0)

# Constants for playing cards
BOARD = []
VILLAN_HAND = Combo('9c8s')
HERO_HAND = Combo('KcKh')

FLOPP = ["Js", "Td", "Qd"]
TURN = ["Qc"]
RIVER = [cards.convertCardName("Ace","Clubs")]

BOARD = FLOPP

strOdds, strHand = odd.probabilityFLOP(BOARD, HERO_HAND, None)

print(strOdds)
print(strHand)

BOARD = BOARD + TURN

strOdds, strHand = odd.probabilityTURN(BOARD, HERO_HAND, None)

print(strOdds)
print(strHand)

BOARD = BOARD + RIVER

strOdds, strHand = odd.probabilityRIVER(BOARD, HERO_HAND, None)

print(strOdds)
print(strHand)

strWinner = odd.findWINNER(BOARD, HERO_HAND, VILLAN_HAND)
print(strWinner)





# Read in Image resize it and convert to grayscale
ImageOriginal = cv.imread("PicturesOfCards/opencv_frame_2.png")     # Works best for a darker background
ImageOriginalResized = cv.resize(ImageOriginal, dsize=(0, 0), fy=RESIZE_FACTOR, fx=RESIZE_FACTOR)


ListOfCardContours = []
ListOfCards = []

PreProcessedPicture = pV.preProcessPicture(ImageOriginalResized)
#ListOfContours = pV.findContours(PreProcessedPicture) # Just searched for contours is obsolet
CardFound, ListOfCardContours = pV.findCards(PreProcessedPicture, CARD_MIN_AREA, CARD_MAX_AREA) # Picture, min area / max area

if CardFound:
    imgList, imgRanksList, imgSuitsList = pV.searchRanksSuits(ImageOriginalResized, ListOfCardContours)

    # Write Values to instances of Cards
    for i in range(len(ListOfCardContours)):
        cX, cY = pV.findCenterpoints(ListOfCardContours[i])
        suit, rank = pV.identifyCard(imgSuitsList[i], imgRanksList[i])
        ListOfCards.append(cards.CardProperties(imgList[i], imgRanksList[i], imgSuitsList[i], cX, cY, rank, suit))

        cv.drawMarker(ImageOriginalResized, (cX, cY), COLOR_BLUE)
        pV.commentImage(ImageOriginalResized, rank, suit, cX, cY)


    # draw contour to image
    cv.drawContours(ImageOriginalResized, ListOfCardContours, -1, COLOR_BLUE, 3)

    # Show all the cards
    #for i in range(len(ListOfCards)):
    #    cv.imshow("Card %i" %i, ListOfCards[i].img)
    #    cv.imshow("Suit %i" %i, ListOfCards[i].suit_img)
    #    cv.imshow("Rank %i" %i, ListOfCards[i].rank_img)

RoI_board, RoI_player1, RoI_player2, board_named = pV.segmentImage(ImageOriginalResized,1920,1080,0.31)
cv.imshow("RoI Board",RoI_board)
cv.imshow("RoI Player1",RoI_player1)
cv.imshow("RoI Player2",RoI_player2)
cv.imshow("Board named",board_named)


# Show Image on Display
cv.imshow('Original Picture', ImageOriginalResized)
cv.waitKey(0)
cv.destroyAllWindows()
