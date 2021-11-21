# ------ Import libaries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# TODO: Read from Camera -> Test with pictures loaded from Computer

ImageGrayscale = cv.imread("PicturesOfCards/Aces_1.jpg", cv.IMREAD_GRAYSCALE)
ImageGrayscaleResized = cv.resize(ImageGrayscale, dsize=(0, 0), fy=0.5, fx=0.5)

cv.imshow('Binary Image with iterative clustering', ImageGrayscaleResized)
cv.waitKey(0)
cv.destroyAllWindows()
