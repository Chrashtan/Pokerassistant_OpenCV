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
ImageGrayscale = cv.imread("PicturesOfCards/Aces_2.jpg", cv.IMREAD_GRAYSCALE)
ImageGrayscaleResized = cv.resize(ImageGrayscale, dsize=(0, 0), fy=0.50, fx=0.50)

# Preprocess image
ImgGauß = cv.GaussianBlur(ImageGrayscaleResized, (11, 11), 0)
ImgSmooth = cv.medianBlur(ImgGauß, 9)
ret, ImageBinarised = cv.threshold(ImageGrayscaleResized, 0, 255, cv.THRESH_OTSU)

# Process Image using Canny
ImgCanny = cv.Canny(ImageGrayscaleResized, 30, 150)
ImgEdged = cv.Canny(ImgGauß, 30, 150)

# Find Contours
CardContours, hierachyf = cv.findContours(ImageBinarised, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# draw contour to image and display
cv.drawContours(ImageGrayscaleResized, CardContours, -1, (0, 255, 0), 3)
cv.imshow('Smooth', ImgSmooth)
cv.imshow('Binary', ImageBinarised)
cv.imshow('Canny', ImgCanny)
cv.imshow('Canny blurred', ImgEdged)
# Print Number of Contours found in the image
print(len(CardContours))

cv.imshow('Original Picture', ImageGrayscaleResized)
cv.waitKey(0)
cv.destroyAllWindows()
