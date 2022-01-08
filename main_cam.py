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


# Constants
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

CARD_MIN_AREA = 0
CARD_MAX_AREA = 0

COLOR_GREEN = (69, 200, 43)
COLOR_BLUE = (255, 0, 0)

CAM_ID = 2


# ----- FOREVER LOOP -----
# Generation of an captured object
WebCam = cv.VideoCapture(CAM_ID)

# Set resolution
WebCam.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
WebCam.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
WebCam.set(cv.CAP_PROP_FPS, 60)


# repeat the following lines as long as the Webcam is accessibley
while WebCam.isOpened():
    # Reading a single image from the WebCam
    Return, Image = WebCam.read()

    # Check whether image was captured
    if Return:


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
                ListOfCards.append(cards.CardProperties(imgList[i], imgRanksList[i], imgSuitsList[i]))
                cX, cY = pV.findCenterpoints(ListOfCardContours[i])
                ListOfCards[i].centerpoint_X = cX
                ListOfCards[i].centerpoint_Y = cY
                suit, rank = pV.identifyCard(imgSuitsList[i], imgRanksList[i])
                ListOfCards[i].rank_name = rank
                ListOfCards[i].suit_name = suit
                cv.drawMarker(Image, (cX, cY), COLOR_BLUE)
                pV.commentImage(Image, rank, suit, cX, cY)

        # Draw box on Live video
        cv.drawContours(Image, ListOfContours, -1, COLOR_GREEN, 1)
        cv.drawContours(Image, ListOfCardContours, -1, COLOR_BLUE, 3)


        cv.putText(Image, "FPS: " + str(int(WebCam.get(cv.CAP_PROP_FPS))), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, COLOR_GREEN, 2,
                   cv.LINE_AA)

        # Show live Video
        cv.imshow("My Video", Image)
        cv.imshow("Pre", PreProcessedPicture)




        key = cv.waitKey(1)
        # First ask for calibration
        if  key == ord('c'):
            CARD_MIN_AREA, CARD_MAX_AREA = pV.calibrateCam(Image)
        elif key == ord('q'):
            break




# Close all windows
cv.destroyAllWindows()
