# ------ Import libaries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def drawBigContours(image):
    """Process Image to grayscale and use the canny algorithm to draw contours into picture"""
    # Process Image
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Using GaussianBlur to delete structures in the Background
    blurred = cv.GaussianBlur(gray, (11, 11), 2)

    # Process Image using Canny
    # How Canny works
    # 1. Apply Gaussian filter to smooth the image in order to remove the noise
    # 2. Find the intensity gradients of the image
    # 3. Apply gradient magnitude thresholding or lower bound cut-off suppression
    #    to get rid of spurious response to edge detection
    # 4. Apply double threshold to determine potential edges
    # 5. Track edge by hysteresis: Finalize the detection of edges by suppressing
    #    all the other edges that are weak and not connected to strong edges.
    edged = cv.Canny(blurred, 30, 150)
    contours, hierachyf = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Sort contours by size -> biggest contour ist at the beginn of the array
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # If no contours are found print an error
    if len(contours) == 0:
        print("No contours found!")
        quit()

    # Find centre of Contours

    # Remove small fragment contours
    cards = []   # Big countours = cards
    for i in range(0, len(contours)):
        if cv.contourArea(contours[i]) > 100000:
            cards.append(contours[i])

    # Find Moments and compute centerpoints
    for cont in cards:
        print(cv.contourArea(cont))
        cont_moments = cv.moments(cont).copy()
        cv.contourArea(cont)
        if cont_moments["m00"] != 0:
            cont_centre_x = int(cont_moments["m10"] / cont_moments["m00"])
            cont_centre_y = int(cont_moments["m01"] / cont_moments["m00"])
            cv.drawMarker(image, (cont_centre_x, cont_centre_y), (69, 200, 43))

    # Momentan werden 8 "Karten" erkannt.
    for i in range(0, len(cards)):
        # Approximate the corner points of the card
        peri = cv.arcLength(cards[i], True)                     # Find angle of tilted card
        approx = cv.approxPolyDP(cards[i], 0.01*peri, True)     # Adjust picture so it fits into a rectangle
        pts = np.float32(approx)
        x, y, w, h = cv.boundingRect(cards[i]) # Draw a rectangle around card.
        # Cut out everything exept the card
        imageCards = image[y:y + h, x:x + w]
        cv.imshow("T", imageCards)



    # draw contour to image
    cv.drawContours(image, cards, -1, (69, 200, 43), 3)







