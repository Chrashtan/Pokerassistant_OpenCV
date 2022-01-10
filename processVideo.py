# ------ Import libaries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import cards

# Constants
BKG_THRESHOLD = 60

def preProcessPicture(image):
    # Process Image
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Using GaussianBlur to delete structures in the Background
    blurred = cv.GaussianBlur(gray, (5, 5), 2)

    # The following code is there to adapt the threshold to the lighting
    # A background pixel in the center top of the video is used to determinde the intensity
    # This allows the threshhold to adapt to the lighting conditions
    img_w, img_h = np.shape(image)[:2] # Maybe another pos?
    bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
    thresh_level = bkg_level + BKG_THRESHOLD # 50 = Background Threshold
    # TODO Background Threshold RoI
    retval, thresh = cv.threshold(blurred, thresh_level, 255, cv.THRESH_BINARY)
    return thresh

def findContours(image):
    """Finds all contours in a picture and returns them into a list"""
    contours, hierachyf = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Chain approx simple saves only 2 points of a contour
    # Sort contours by size -> biggest contour is at the beginn of the array
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    # print(cv.contourArea(contours[0])) just for debugging
    # If no contours are found print an error
    if len(contours) == 0:
        # print("No contours found!")
        return []
    else:
       return contours


def findCards(image, min_area, max_area):
    """Gets a picture and min and max area for one Card. Returns a List of card contours.
    Also Returns a Flag -> CardFound"""
    ListOfCardContours = []  # Big countours = cards
    CardFound = False

    contours, hierachyf = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Sort contours by size -> biggest contour is at the beginn of the array
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # If no contour is found, do nothing
    if len(contours) == 0:
        # print("No contours found!")
        CardFound = False
        return CardFound, []
    else:
        for i in range(len(contours)):
            size = cv.contourArea(contours[i])
            peri = cv.arcLength(contours[i], True)
            approx = cv.approxPolyDP(contours[i], 0.01*peri, True)

            # contour is card if:
            # - contour is smaller than max area
            # - contour area is greater than min are
            # - have 4 corners
            if((size < max_area) and (size > min_area) and (len(approx) == 4)):
                #ListOfCardContours.append(contours[i])
                ListOfCardContours.append(approx)
                CardFound = True

        return CardFound, ListOfCardContours


def findCenterpoints(card):
    """Returns centerpoint of one card"""
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

    for i in range(0, len(imgList)):
        # take important parts out of the transformed image:
        height = imgList[i].shape[0]
        width = imgList[i].shape[1]
        YCut1 = int(15 / 446 * height) # recalculate the cut values for correct card size
        YCut2 = int(70 / 446 * height) # könnte man auch teilweise auslagern bzw constant machen
        YCut3 = int(115 / 446 * height)
        XCut1 = int(5 / 320 * width)
        XCut2 = int(40 / 320 * width)

        imgRanksList.append(imgList[i][YCut1:YCut2, XCut1:XCut2]) # Das als Konstante? also SUITS_WIDTH = 15:70 ?
        imgSuitsList.append(imgList[i][YCut2:YCut3, XCut1:XCut2])

    return imgList, imgRanksList, imgSuitsList


# Brauchen wir das?
def identifyCard(imgSuit, imgRank):
    rank = identifyImage(imgRank, True)
    suit = identifyImage(imgSuit, False)

    return suit, rank


def identifyImage(img, isRank):
    """Identifies the card rank or suit, needs image of rank or image of suit, isRank = True if searching for rank, returns best match"""

    imgPre = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    thresh, imgPre = cv.threshold(imgPre, 0, 255, cv.THRESH_BINARY_INV +cv.THRESH_OTSU)
    array_cont,x = cv.findContours(imgPre, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if len(array_cont) == 0:
        return " "
    x, y, w, h = cv.boundingRect(array_cont[0])  # Draw a rectangle around card.
    # Cut out everything exept the card
    imgCut = imgPre[y:y + h, x:x + w]
    height = imgCut.shape[0]
    width = imgCut.shape[1]
    bestFit = 1000
    # Define the image references depends on the flag
    if isRank:
        imgRefs = cards.RANK_REFS
    else:
        imgRefs = cards.SUIT_REFS

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
    cv.imshow("cut", imgCut)
    cv.imshow("in", imgPre)
    #imgSolved = cv.imread("Card_Imgs/"+result+".jpg")
    #imgSolved = cv.resize(imgSolved, (width, height))
    #cv.imshow("Best Fit", imgSolved)
    return result

def calibrateCam(frame):
    """Gets a Frame from the Webcam and search for contour"""
    # Draw Text to help the user to draw his RoI
    HelpText = "Please mark ONE card and press the SPACEBAR or ENTER"
    font = cv.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    # Call putText 2 times to draw contour to text
    cv.putText(frame, HelpText, (60,60), font, fontScale, (0,0,0), 3, cv.LINE_AA)
    cv.putText(frame, HelpText, (60,60), font, fontScale, (50,200,200), 2, cv.LINE_AA)
    # Find Contour
    binFrame = preProcessPicture(frame)
    # SPACE pressed
    RoI = cv.selectROI('Please select ROI:', frame)
    x = RoI[0]  # x coordinate of top-left corner point of ROI
    y = RoI[1]  # y coordinate of top-left corner point of ROI
    w = RoI[2]  # Width of RoI
    h = RoI[3]  # Height of RoI
    # ------------- Create my RoI Image ------------------
    RoIImage = frame[y:y + h, x:x + w]
    RoIBin = preProcessPicture(RoIImage)
    RoIcnt = findContours(RoIBin)

    # Uses the Card Area to calculate min and max Area for a Card
    cardArea = round(cv.contourArea(RoIcnt[0]))  # Card is biggest contour so at pos 0
    minArea = round(cardArea - (0.1 * cardArea))  # subract 10%
    maxArea = round(cardArea + (0.1 * cardArea))  # add 10%
    print("Contour Area: ", cardArea)
    print("Card min Area: ", minArea)
    print("Card max Area: ", maxArea)
    cv.destroyWindow("Please select ROI:")
    return minArea, maxArea

def commentImage(image, rankName, suitName, x, y):
    """"Draw a comment in a picture"""
    font = cv.FONT_HERSHEY_SIMPLEX  # font
    fontScale = 1  # fontScale
    color = (255, 0, 0)  # Blue color in BGR
    thickness = 2  # Line thickness of 2 px
    # position = (50, 50) # position
    # Using cv2.putText() method
    # Draw card name twice, so letters have black outline
    cv.putText(image, rankName,(x-60,y-10), font, fontScale,(0,0,0), 3, cv.LINE_AA)
    cv.putText(image, rankName,(x-60,y-10), font, fontScale,(50,200,200), 2, cv.LINE_AA)

    cv.putText(image, suitName,(x-60,y+25), font, fontScale,(0,0,0), 3, cv.LINE_AA)
    cv.putText(image, suitName,(x-60,y+25), font, fontScale,(50,200,200), 2, cv.LINE_AA)


def segmentImage(image, img_width, img_height, size_board_RoI):
    """Segments the image in 3 Images. Needs the image, the width, the height
    and a size of the RoI (in percent). Returns 3 Images"""
    RoI_Board_midline = int(img_height/2)

    # coordinates with index1: corner top left
    # coordinates with index2: corner bottom right

    #Board
    x1_b = 0
    y1_b = int(RoI_Board_midline * (1-size_board_RoI))
    x2_b = img_width
    y2_b = int(RoI_Board_midline * (size_board_RoI+1.05))
    #Player1
    x1_1 = 0
    y1_1 = int(RoI_Board_midline * (size_board_RoI+1))
    x2_1 = img_width
    y2_1 = img_height
    # Player2
    x1_2 = 0
    y1_2 = 0
    x2_2 = img_width
    y2_2 = int(RoI_Board_midline * (1-size_board_RoI))

    # Draw board areas
    cv.rectangle(image, (x1_b, y1_b), (x2_b, y2_b), (0, 255, 0), 2)
    # Draw the area name
    font = cv.FONT_HERSHEY_SIMPLEX  # font
    fontScale = 1  # fontScale
    board_named = cv.putText(image, "Board", (10, RoI_Board_midline), cv.FONT_HERSHEY_SIMPLEX, 1, (69, 200, 43), 3, cv.LINE_AA)
    board_named = cv.putText(image, "Player2", (10, int(y2_2/2)), cv.FONT_HERSHEY_SIMPLEX, 1, (69, 200, 43), 3, cv.LINE_AA)
    board_named = cv.putText(image, "Player1", (10, int((img_height-y2_b)/2)+y2_b), cv.FONT_HERSHEY_SIMPLEX, 1, (69, 200, 43), 3, cv.LINE_AA)


    RoI_Board = image[y1_b:y2_b, x1_b:x2_b]
    RoI_Player1 = image[y1_1:y2_1, x1_1:x2_1]
    RoI_Player2 = image[y1_2:y2_2, x1_2:x2_2]

    return RoI_Board, RoI_Player1, RoI_Player2, board_named






#draw.box fkt.



    




