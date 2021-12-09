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
    imgList = []
    # Momentan werden 8 "Karten" erkannt.
    for i in range(0, len(cards)):
        # Approximate the corner points of the card
        peri = cv.arcLength(cards[i], True)                     # maximum distance from contour to approximated contour
        approx = cv.approxPolyDP(cards[i], 0.01*peri, True)     # Approx contour around object
                                                                # 1% Around Contour -> If bigger less contours get drawn
        pts = np.float32(approx)
        x, y, w, h = cv.boundingRect(cards[i]) # Draw a rectangle around card.
        # Cut out everything exept the card
        imageCards = image[y:y + h, x:x + w]
        cv.imshow("T", imageCards)

        # code for transformation:
        rect = cv.minAreaRect(pts)  # capture smallest possible rectangle (as group of pixels(?))
        boundsBox = cv.boxPoints(rect)
        boundsBox = np.int0(boundsBox)  # turn into integer
        if int(rect[1][1]) > int(rect[1][0]):   # images tilted further than 45° are rotated to stand upright
            boxWidth = int(rect[1][0])
            boxHeight = int(rect[1][1])
            src_pts = boundsBox.astype("float32")   # the transform works by overlapping the source and destination corners
                                                    # which are set up in this step (bound corners and new image corners)
            dst_pts = np.array([[0, boxHeight-1], [0, 0], [boxWidth-1, 0], [boxWidth-1, boxHeight-1]], dtype="float32")
        else:
            boxWidth = int(rect[1][1])
            boxHeight = int(rect[1][0])
            src_pts = boundsBox.astype("float32")
            dst_pts = np.array([[0, 0], [boxWidth-1, 0], [boxWidth-1, boxHeight-1], [0, boxHeight-1]], dtype="float32")

        # the perspective transformation matrix
        TransformMatrix = cv.getPerspectiveTransform(src_pts, dst_pts)

        # cut and rotate the bounding box to get the upright rectangle
        imgList.append(cv.warpPerspective(image, TransformMatrix, (boxWidth, boxHeight)))

    for i in range(0, len(imgList)):
        cv.imshow('cropped images:', imgList[i])

    # draw contour to image
    cv.drawContours(image, cards, -1, (69, 200, 43), 3)







