# ------ Import libaries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import cards

def preProcessPicture(image):
    # Process Image
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Using GaussianBlur to delete structures in the Background
    blurred = cv.GaussianBlur(gray, (11, 11), 2)

    # The following code is there to adapt the threshold to the lighting
    # A background pixel in the center top of the video is used to determinde the intensity
    # This allows the threshhold to adapt to the lighting conditions
    img_w, img_h = np.shape(image)[:2]
    bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
    thresh_level = bkg_level + 50

    retval, thresh = cv.threshold(blurred, thresh_level, 255, cv.THRESH_BINARY)
    return thresh

def findContours(image):
    """Finds all contours in a picture and returns them into a list"""
    # Process Image using Canny
    #edged = cv.Canny(image, 50, 150)
    contours, hierachyf = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Chain approx simple saves only 2 points of a contour
    # Sort contours by size -> biggest contour is at the beginn of the array
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # If no contours are found print an error
    if len(contours) == 0:
        print("No contours found!")
        quit()
    else:
        return contours

def findCards(image, min_area, max_area):
    """Gets a picture and min and max area for one Card. Returns a List of card contours"""
    ListOfCardContours = []  # Big countours = cards

    contours, hierachyf = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Sort contours by size -> biggest contour is at the beginn of the array
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # If no contour, do nothing
    if len(contours) == 0:
        return []

    for i in range(len(contours)):
        size = cv.contourArea(contours[i])
        peri = cv.arcLength(contours[i], True)
        approx = cv.approxPolyDP(contours[i], 0.01*peri, True)

        # contour is card if:
        # - contour is smaller than max area
        # - contour area is greater than min are
        # - have 4 corners
        if((size < max_area) and (size > min_area) and (len(approx) == 4)):
            ListOfCardContours.append(contours[i])

    return ListOfCardContours



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


imgRefs = ["Ace","Clubs","Diamonds","Eight","Five","Four","Hearts","Jack","King","Nine","Queen","Seven","Six","Spades","Ten","Three","Two"]


def identifyCard(imgSuit, imgRank):
    rank = cards.CardRanks
    suit = cards.CardSuits
    rank = identifyImage(imgRank)
    suit = identifyImage(imgSuit)

    return suit, rank


def identifyImage(img):
    """Identifies the card rank or suit, needs image of rank or image of suit, returns best match"""
    imgPre = preProcessPicture(img)
    thresh, imgPre = cv.threshold(imgPre, 0, 255, cv.THRESH_BINARY_INV +cv.THRESH_OTSU)
    array_cont,x = cv.findContours(imgPre, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    x, y, w, h = cv.boundingRect(array_cont[0])  # Draw a rectangle around card.
    # Cut out everything exept the card
    imgCut = imgPre[y:y + h, x:x + w]
    cv.imshow("cut", imgCut)
    height = imgCut.shape[0]
    width = imgCut.shape[1]
    bestFit = 1000
    for ref in imgRefs:
        imgSample = cv.imread("Card_Imgs/"+ref+".jpg")
        imgSample = imgSample[:,:,0]
        imgSample = cv.resize(imgSample, (width, height))

        imgDiff = cv.subtract(imgCut, imgSample)  # The difference has to be taken twice, once for pixels
        currentFit = np.sum(imgDiff == 255)  # that are missing in the sample, once for those that
        imgDiff = cv.subtract(imgSample, imgCut)  # are not supposed to be there
        currentFit = currentFit + np.sum(imgDiff == 255)

        if currentFit<bestFit:
            bestFit = currentFit
            result = ref
    # just for checking the result
    imgSolved = cv.imread("Card_Imgs/"+result+".jpg")
    imgSolved = cv.resize(imgSolved, (width, height))
    cv.imshow("Best Fit", imgSolved)

    return result

