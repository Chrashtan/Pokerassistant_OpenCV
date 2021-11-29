# ------ Import libaries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import cards


def drawContours(image):
    """Process Image to grayscale and use the canny algorithm to draw contours into picture"""
    # Process Image
    image_grayscale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Using GaussianBlur to delete structures in the Background
    img_gauss = cv.GaussianBlur(image_grayscale, (11, 11), 2)

    # Process Image using Canny
    # How Canny works
    # 1. Apply Gaussian filter to smooth the image in order to remove the noise
    # 2. Find the intensity gradients of the image
    # 3. Apply gradient magnitude thresholding or lower bound cut-off suppression
    #    to get rid of spurious response to edge detection
    # 4. Apply double threshold to determine potential edges
    # 5. Track edge by hysteresis: Finalize the detection of edges by suppressing
    #    all the other edges that are weak and not connected to strong edges.
    img_edged = cv.Canny(img_gauss, 30, 150)
    edged_contours, hierachyf = cv.findContours(img_edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Find centre of Contours

    # Remove small fragment contours
    big_contours = []
    for i in range(0, len(edged_contours)):
        if cv.contourArea(edged_contours[i]) > 100000:
            big_contours.append(edged_contours[i])

    # Find Moments and compute centerpoints
    for cont in big_contours:
        print(cv.contourArea(cont))
        cont_moments = cv.moments(cont).copy()
        cv.contourArea(cont)
        if cont_moments["m00"] != 0:
            cont_centre_x = int(cont_moments["m10"] / cont_moments["m00"])
            cont_centre_y = int(cont_moments["m01"] / cont_moments["m00"])
            cv.drawMarker(image, (cont_centre_x, cont_centre_y), (69, 200, 43))

    # draw contour to image
    # cv.drawContours(ImageOriginalResized, CardContours, -1, (0, 255, 0), 3)
    cv.drawContours(image, big_contours, -1, (69, 200, 43), 3)

    # TODO: returnvalue of found contours


