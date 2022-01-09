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

CAM_ID = 2


MAX_AGE = 20
SAME_CARD_RADIUS = 60
NUMBER_TO_AVERAGE = 10

# ----- FOREVER LOOP -----
# Generation of an captured object
WebCam = cv.VideoCapture(CAM_ID)

# Set resolution
WebCam.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
WebCam.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
WebCam.set(cv.CAP_PROP_FPS,30)

# store cards and values of previous iterations
recognizedCards = []
readSuits = [[]]
readRanks = [[]]

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

                cv.drawMarker(Image, (cX, cY), COLOR_BLUE)
                pV.commentImage(Image, rank, suit, cX, cY) # TODO: Reinschreiben nach der Auswertung

            # Segment image
            # Board RoI
            # Show SUIT and RANK in the same Window
            # Hori = np.concatenate((ListOfCards[0].suit_img, ListOfCards[0].rank_img), axis=1) # they dont have the same dimensions
            # cv.imshow("RANK / SUIT", Hori)

            # test for adding the cards etc
            for i in range(0,len(ListOfCards)):
                flagIsInCircle = False
                for j in range(0,len(recognizedCards)):
                    # is the centrepoint of any of the found cards close to the centrepoint of one of the old ones?
                    if (pV.pointInCircle((ListOfCards[i].centerpoint_X,ListOfCards[i].centerpoint_Y),SAME_CARD_RADIUS,(recognizedCards[j].centerpoint_X,recognizedCards[j].centerpoint_Y))):
                        flagIsInCircle = True
                        recognizedCards[j]= ListOfCards[i] # then replace that card with the newly found one
                        # which is hopefully the same card but slightly moved
                if flagIsInCircle == False:
                    recognizedCards.append(ListOfCards[i]) # otherwise add a new cardspot for it

            for i in range(0, len(ListOfCards)):
                if ListOfCards[i].cycle_age > MAX_AGE: # card has not been found in a while so it will be removed
                    ListOfCards.remove(ListOfCards[i])
                    readRanks.remove(readRanks[i])
                    readSuits.remove(readSuits[i])
                else:
                    ListOfCards[i].cycle_age = ListOfCards[i].cycle_age + 1
                    readRanks[i].append(ListOfCards[i].rank_name) # the ranks and suits are stored with the values
                    readRanks[i].append(ListOfCards[i].suit_name) # that have been found on previous iterations
                                                                  # so that the result can be averaged out


            # # Just temp
            # if len(ListOfCards) > 0:
            #     print(pV.identifyImage(ListOfCards[0].rank_img, True))
            #     # print(pV.identifyImage(ListOfCards[0].suit_img, False))
            #
            #     cv.imshow("Card 0", ListOfCards[i].img)
            #     cv.imshow("Suit 0", ListOfCards[i].suit_img)
            #     cv.imshow("Rank 0", ListOfCards[i].rank_img)
            # else:
            #     cv.destroyWindow("Card 0")
            #     cv.destroyWindow("Suit 0")
            #     cv.destroyWindow("Rank 0")



        # Draw box on Live video
        #cv.drawContours(Image, ListOfContours, -1, COLOR_GREEN, 1)
        cv.drawContours(Image, ListOfCardContours, -1, COLOR_BLUE, 3)

        # read out enttime
        endtime = time.time()
        timeDiff = endtime-startTime
        framerate = 1.0 / timeDiff

        cv.putText(Image, "FPS: " + str(int(framerate)), (100, 200), cv.FONT_HERSHEY_SIMPLEX, 1, COLOR_GREEN, 2,
                   cv.LINE_AA)

        # Show live Video
        cv.imshow("My Video", Image)
        #cv.imshow("Pre", PreProcessedPicture)


        key = cv.waitKey(50)
        # First ask for calibration
        if  key == ord('c'):
            CARD_MIN_AREA, CARD_MAX_AREA = pV.calibrateCam(Image)
        elif key == ord('q'):
            break




# Close all windows
cv.destroyAllWindows()


