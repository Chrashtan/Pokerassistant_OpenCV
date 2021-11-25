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

# TODO: Read from Camera -> Test with pictures loaded from Computer
# Read in Image resize it and convert to grayscale
ImageOriginal = cv.imread("PicturesOfCards/Aces_4.jpg") # Works best for a darker background
ImageOriginalResized = cv.resize(ImageOriginal, dsize=(0, 0), fy=0.50, fx=0.50)
ImageGrayscale = cv.cvtColor(ImageOriginalResized, cv.COLOR_BGR2GRAY)


# Using GaussianBlur to delete structures in the Background
ImgGauß = cv.GaussianBlur(ImageGrayscale, (11, 11), 2)
# Smooth out the Blurred image
ImgSmooth = cv.medianBlur(ImgGauß, 9)
# Binarise the Image
ret, ImageBinarised = cv.threshold(ImageGrayscale, 0, 255, cv.THRESH_OTSU)

# Process Image using Canny
# How Canny works
# 1. Apply Gaussian filter to smooth the image in order to remove the noise
# 2. Find the intensity gradients of the image
# 3. Apply gradient magnitude thresholding or lower bound cut-off suppression
#    to get rid of spurious response to edge detection
# 4. Apply double threshold to determine potential edges
# 5. Track edge by hysteresis: Finalize the detection of edges by suppressing
#    all the other edges that are weak and not connected to strong edges.

ImgCanny = cv.Canny(ImageGrayscale, 30, 150)
ImgEdged = cv.Canny(ImgGauß, 30, 150)

# Find Contours
CardContours, hierachyf = cv.findContours(ImgEdged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
EdgedContours, hierachyf = cv.findContours(ImgEdged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


# Find centre of Contours

# Remove small fragment contours
BigContours = []
for i in range(0, len(EdgedContours)):
    if cv.contourArea(EdgedContours[i]) > 100000:
        BigContours.append(EdgedContours[i])

# Find Moments and compute Centrepoints
for cont in BigContours:
    print(cv.contourArea(cont))
    ContMoments = cv.moments(cont).copy()
    cv.contourArea(cont)
    if ContMoments["m00"] != 0:
        ContCentreX = int(ContMoments["m10"]/ContMoments["m00"])
        ContCentreY = int(ContMoments["m01"]/ContMoments["m00"])
        cv.drawMarker(ImageOriginalResized, (ContCentreX, ContCentreY), (69, 200, 43))


# draw contour to image
#cv.drawContours(ImageOriginalResized, CardContours, -1, (0, 255, 0), 3)
cv.drawContours(ImageOriginalResized, BigContours, -1, (69, 200, 43), 3)


# Show Image on Display
# cv.imshow('Smooth', ImgSmooth)
# cv.imshow('Binary', ImageBinarised)
# cv.imshow('Canny', ImgCanny)
cv.imshow('Canny blurred', ImgEdged)


# Print Number of Contours found in the image
print(len(CardContours))
print(len(EdgedContours[1]))
cv.imshow('Original Picture', ImageOriginalResized)
cv.waitKey(0)
cv.destroyAllWindows()
