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




# ----- FOREVER LOOP -----
# TODO: Read from Camera -> Test with pictures loaded from Computer
# Read in Image resize it and convert to grayscale
ImageOriginal = cv.imread("PicturesOfCards/Aces_4.jpg")     # Works best for a darker background
ImageOriginalResized = cv.resize(ImageOriginal, dsize=(0, 0), fy=0.50, fx=0.50)

# TODO: ADD FOREVER LOOP WITH LIVE VIDEO FEED
ListOfCardContours = []
ListOfCards = []

PreProcessedPicture = pV.preProcessPicture(ImageOriginalResized)
ListOfContours = pV.findContours(PreProcessedPicture)
ListOfCardContours = pV.findCards(ListOfContours)

imgList, imgRanksList, imgSuitsList = pV.searchRanksSuits(ImageOriginalResized, ListOfCardContours)

# Write Values to instances of Cards
for i in range(len(ListOfCardContours)):
    ListOfCards.append(cards.CardProperties(imgList[i], imgRanksList[i], imgSuitsList[i]))
    cX, cY = pV.findCenterpoints(ListOfCardContours[i])
    ListOfCards[i].centerpoint_X = cX
    ListOfCards[i].centerpoint_Y = cY


# Draw in contours and Centerpoint in Orginal picture
for i in range(len(ListOfCards)):
    cv.drawMarker(ImageOriginalResized, (ListOfCards[i].centerpoint_X, ListOfCards[i].centerpoint_Y), (69, 200, 43))

# draw contour to image
cv.drawContours(ImageOriginalResized, ListOfCardContours, -1, (69, 200, 43), 3)


# Show all the cards
for i in range(len(ListOfCards)):
    cv.imshow("Card %i" %i, ListOfCards[i].img)
    cv.imshow("Suit %i" %i, ListOfCards[i].suit_img)
    cv.imshow("Rank %i" %i, ListOfCards[i].rank_img)



# Show Image on Display
cv.imshow('Original Picture', ImageOriginalResized)
cv.waitKey(0)
cv.destroyAllWindows()
