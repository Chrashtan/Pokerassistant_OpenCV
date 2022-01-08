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
import processVideo
import processVideo as pV

# Constants
CARD_MIN_AREA = 59072
CARD_MAX_AREA = 72200

RESIZE_FACTOR = 1

COLOR_GREEN = (69, 200, 43)
COLOR_BLUE = (255, 0, 0)



# Read in Image resize it and convert to grayscale
ImageOriginal = cv.imread("PicturesOfCards/opencv_frame_0.png")     # Works best for a darker background
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
        ListOfCards.append(cards.CardProperties(imgList[i], imgRanksList[i], imgSuitsList[i]))
        cX, cY = pV.findCenterpoints(ListOfCardContours[i])
        ListOfCards[i].centerpoint_X = cX
        ListOfCards[i].centerpoint_Y = cY


    # Draw in contours and Centerpoint in Orginal picture
    for i in range(len(ListOfCards)):
        cv.drawMarker(ImageOriginalResized, (ListOfCards[i].centerpoint_X, ListOfCards[i].centerpoint_Y), COLOR_GREEN)

    # draw contour to image
    cv.drawContours(ImageOriginalResized, ListOfCardContours, -1, COLOR_BLUE, 3)

    # Show all the cards
    for i in range(len(ListOfCards)):
        cv.imshow("Card %i" %i, ListOfCards[i].img)
        cv.imshow("Suit %i" %i, ListOfCards[i].suit_img)
        cv.imshow("Rank %i" %i, ListOfCards[i].rank_img)


    testSuit, testRank = pV.identifyCard(imgSuitsList[0], imgRanksList[0])

                                                                #y-koordinate - bisschen mehr hälfte der Kartehöhe: ListOfCards[2].centerpoint_X,ListOfCards[2].centerpoint_Y-40)
pV.commentImage("Card_Imgs/Ace.jpg","dfsfgsdg",(10,40))

# Show Image on Display
cv.imshow('Original Picture', ImageOriginalResized)
cv.waitKey(0)
cv.destroyAllWindows()
