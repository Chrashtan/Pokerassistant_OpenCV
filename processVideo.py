# ------ Import libaries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def preProcessPicture(image):
    # Process Image
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Using GaussianBlur to delete structures in the Background
    blurred = cv.GaussianBlur(gray, (11, 11), 2)
    return blurred

def findContours(image):
    """Finds all contours in a picture and returns them into a list"""
    # Process Image using Canny
    edged = cv.Canny(image, 20, 150)
    contours, hierachyf = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Sort contours by size -> biggest contour is at the beginn of the array
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    # If no contours are found print an error
    if len(contours) == 0:
        print("No contours found!")
        quit()
    else:
        return contours

def findCards(contours):
    """Gets a list of contours and filters all small contours"""
    # Remove small fragment contours
    ListofCardContours = []   # Big countours = cards
    for i in range(0, len(contours)):
        if cv.contourArea(contours[i]) > 100000:
            ListofCardContours.append(contours[i])
    return ListofCardContours

def findCenterpoints(card):
    """Returns centerpoint of one card"""
    print(cv.contourArea(card))
    cont_moments = cv.moments(card).copy()
    cv.contourArea(card)
    if cont_moments["m00"] != 0:
        cont_centre_x = int(cont_moments["m10"] / cont_moments["m00"])
        cont_centre_y = int(cont_moments["m01"] / cont_moments["m00"])
    return cont_centre_x, cont_centre_y


def searchRanksSuits(image, CardContours):
    """Search Ranks and Suits in the Orginal image. Needs Orginal image and Contours of the Cards, returns
    image of the card, image of the rank and image of the suit"""

    imgList = []        # warum sind die hier als matrix definiert, wird nicht nur ein card image verarbeitet?
    imgSuitsList = []
    imgRanksList = []

    for i in range(0, len(CardContours)):
        # Approximate the corner points of the card
        peri = cv.arcLength(CardContours[i], True)                     # maximum distance from contour to approximated contour
        approx = cv.approxPolyDP(CardContours[i], 0.01*peri, True)     # Approx contour around object
                                                                # 1% Around Contour -> If bigger less contours get drawn
        pts = np.float32(approx)
        x, y, w, h = cv.boundingRect(CardContours[i]) # Draw a rectangle around card.
        # Cut out everything exept the card
        imageCards = image[y:y + h, x:x + w]

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

    # take important parts out of the transformed image:

    for i in range(0, len(imgList)):
        imgSuitsList.append(imgList[i][15:70, 5:40])
        imgRanksList.append(imgList[i][70:115, 5:40])

    return imgList, imgRanksList, imgSuitsList

def identifyCard(img):
    """Identifies the card rank or suit, needs image of rank or image of suit, returns best match"""

    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgPre = preProcessPicture(img)
    array_cont = findContours(imgPre)
    print(type(array_cont[1]))

    x, y, w, h = cv.boundingRect(array_cont[0])  # Draw a rectangle around card.
    # Cut out everything exept the card
    imgCut = img[y:y + h, x:x + w]
    cv.drawContours(img, array_cont, -1, (69, 200, 43), 1)
    cv.rectangle(img,  (x, y),(x+w,y+h), (69, 200, 43), 2)
    img = cv.resize(img,dsize=(0,0),dst=0,fx = 4, fy = 4)
    cv.imshow("original", img)
    cv.imshow("cut",imgCut)

# def manualBox(points):
#
#     minY = int
#     minX = int
#     maxY = int
#     maxX = int
#     minY = points[0,0,1]
#     minX = points[0,0,0]
#     maxY = points[0,0,1]
#     maxX = points[0,0,0]
#     for i in range(1, len(points)):
#         if points[i,0,1] > maxY:
#             maxY = points[i,0,1]
#         if points[i,0,0] > maxX:
#             maxX = points[i,0,0]
#         if points[i,0,1] < minY:
#             minY = points[i,0,1]
#         if points[i,0,0] < minX:
#             minX = points[i,0,0]
#
#     return minX, minY, maxX, maxY
