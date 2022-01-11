# ***********************************************
# ***********************************************
# **************** Main script ******************
# ***********************************************
# ***********************************************

# ------ Import libraries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import cards
import processVideo as pV
import time

# Constants
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

CARD_MIN_AREA = 0
CARD_MAX_AREA = 0

COLOR_GREEN = (69, 200, 43)
COLOR_BLUE = (255, 0, 0)
COLOR_BLACK = (0, 0, 0)

CAM_ID = 2

MAX_AGE = 50
SAME_CARD_RADIUS = 10
NUMBER_TO_AVERAGE = 10

# store cards and values of previous iterations
recognizedCards = []
readSuits = [[]]
readRanks = [[]]


# find if a point is inside a a given circle
def pointInCircle(centerX, centerY, radius, pointX, pointY):
    """finds if a point is inside a a given circle"""
    if (((pointX - centerX) * (pointX - centerX)) + ((pointY - centerY) * (pointY - centerY))) < (radius * radius):
        return True
    else:
        return False

def averageValuesforCard(index):
    """Takes the most recognized value from the values in readSuits and readRanks"""
    while len(readRanks[index]) > NUMBER_TO_AVERAGE:
        readRanks[index].remove(readRanks[index][0])

    while len(readSuits[index]) > NUMBER_TO_AVERAGE:
        readSuits[index].remove(readSuits[index][0])

    rankFit = cards.RANK_REFS[0]
    rankCount = 0
    rankMax = readRanks[index].count(cards.RANK_REFS[0])
    suitFit = cards.SUIT_REFS[0]
    suitCount = 0;
    suitMax = readSuits[index].count(cards.SUIT_REFS[0])

    for i in range(1,len(cards.SUIT_REFS)):
        suitCount = readSuits[index].count(cards.SUIT_REFS[i])
        if suitCount > suitMax:
            suitMax = suitCount
            suitFit = cards.SUIT_REFS[i]
    for i in range(1,len(cards.RANK_REFS)):
        rankCount = readRanks[index].count(cards.RANK_REFS[i])
        if rankCount > rankMax:
            rankMax = rankCount
            rankFit = cards.RANK_REFS[i]

    if suitMax < (NUMBER_TO_AVERAGE * 0.7):
        suitFit = "UNKNOWN"

    if rankMax < (NUMBER_TO_AVERAGE * 0.7):
        rankFit = "UNKNOWN"

    return suitFit, rankFit




# ----- FOREVER LOOP -----
# Generation of an captured object
WebCam = cv.VideoCapture(CAM_ID)

# Set resolution
WebCam.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
WebCam.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
WebCam.set(cv.CAP_PROP_FPS,30)



# repeat the following lines as long as the Webcam is accessibley
while WebCam.isOpened():
    # Reading a single image from the WebCam
    Return, Image = WebCam.read()

    # Check whether image was captured
    if Return:
        # Start time for fps Counter
        startTime = time.time()

        # Use Filter on Image
        PreProcessedPicture = pV.preProcessPicture(Image)
        # Find all contures in the Picture and draw them into the picture
        ListOfContours = pV.findContours(PreProcessedPicture)
        # Find cards
        CardFound, ListOfCardContours = pV.findCards(PreProcessedPicture, CARD_MIN_AREA, CARD_MAX_AREA)  # Picture, min area / max area
        # Commit

        # When Card is found draw box around Cards
        if CardFound:
            # Create empty list
            ListOfCards = []

            imgList, imgRanksList, imgSuitsList = pV.searchRanksSuits(Image, ListOfCardContours)

            # Write Values to instances of Cards
            for i in range(len(ListOfCardContours)):
                cX, cY = pV.findCenterpoints(ListOfCardContours[i])
                suit, rank = pV.identifyCard(imgSuitsList[i], imgRanksList[i])
                ListOfCards.append(cards.CardProperties(imgList[i], imgRanksList[i], imgSuitsList[i],
                                                        cX, cY, rank, suit))
                pV.commentImage(Image, rank, suit, cX, cY)
                cv.drawMarker(Image, (cX, cY), COLOR_BLUE)

                # Debugging
                # cv.imshow("Rank", imgRanksList[i])
                # cv.imshow("Suit", imgSuitsList[i])



            # Board, Player1, Player2, BoardName = pV.segmentImage(Image,FRAME_WIDTH,FRAME_HEIGHT, 0.5)

            #cv.imshow("Board", Board)
            #cv.imshow("Player1", Player1)
            #cv.imshow("Player2", Player2)
            #cv.imshow("BoardName", BoardName)
            # Segment image
            # Board RoI
            # Show SUIT and RANK in the same Window


        # Draw box on Live video
        #cv.drawContours(Image, ListOfContours, -1, COLOR_GREEN, 2)
        cv.drawContours(Image, ListOfCardContours, -1, COLOR_BLUE, 3)

        # read out enttime
        endtime = time.time()
        timeDiff = endtime-startTime
        framerate = 1.0 / timeDiff

        cv.putText(Image, "FPS: " + str(int(framerate)), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, COLOR_BLACK, 3, cv.LINE_AA)
        cv.putText(Image, "FPS: " + str(int(framerate)), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, COLOR_GREEN, 2, cv.LINE_AA)

        # Show live Video
        cv.imshow("My Video", Image)
        # cv.imshow("Pre", PreProcessedPicture)


        key = cv.waitKey(50)
        # First ask for calibration
        if  key == ord('c'):
            CARD_MIN_AREA, CARD_MAX_AREA = pV.calibrateCam(Image)
        elif key == ord('q'):
            break

# Close all windows
cv.destroyAllWindows()

