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
import processVideo as pV

# TODO: Read from Camera -> Test with pictures loaded from Computer
# Read in Image resize it and convert to grayscale
ImageOriginal = cv.imread("PicturesOfCards/Aces_4.jpg")     # Works best for a darker background
ImageOriginalResized = cv.resize(ImageOriginal, dsize=(0, 0), fy=0.50, fx=0.50)
ImageGrayscale = cv.cvtColor(ImageOriginalResized, cv.COLOR_BGR2GRAY)

imgList, imgRanksList, imgSuitsList = pV.searchRanksSuits(ImageOriginalResized)

ListOfCards = []

for i in range(len(imgList)):
    ListOfCards.append(cards.CardProperties(imgList[i], imgRanksList[i], imgSuitsList[i]))

# Show all the cards
for i in range(len(ListOfCards)):
    cv.imshow("Card %i" %i, ListOfCards[i].img)
    cv.imshow("Suit %i" %i, ListOfCards[i].suit_img)
    cv.imshow("Rank %i" %i, ListOfCards[i].rank_img)





# Show Image on Display
cv.imshow('Original Picture', ImageOriginalResized)
cv.waitKey(0)
cv.destroyAllWindows()
