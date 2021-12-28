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

# to Show that the functions works
# Show all cropped cards
for i in range(0, len(imgList)):
    cv.imshow("cropped image %i:" % i, imgList[i])

# Show all the Ranks/Suits
for i in range(0, len(imgRanksList)):
    cv.imshow('colour %i' %i, imgSuitsList[i])
    cv.imshow('face %i' % i, imgRanksList[i])




# Show Image on Display
cv.imshow('Original Picture', ImageOriginalResized)
cv.waitKey(0)
cv.destroyAllWindows()
