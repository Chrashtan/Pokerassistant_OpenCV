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

pV.drawBigContours(ImageOriginalResized)



# Show Image on Display

# Print Number of Contours found in the image
# print(len(CardContours))
# print(len(EdgedContours[1]))
cv.imshow('Original Picture', ImageOriginalResized)
cv.waitKey(0)
cv.destroyAllWindows()
