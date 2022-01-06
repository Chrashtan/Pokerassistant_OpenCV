# ***********************************************
# ***********************************************
# **************** Main script ******************
# ***********************************************
# ***********************************************

# ------ Import libaries -------
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import cards
import processVideo as pV


# Constants
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

CARD_MIN_AREA = 100000
CARD_MAX_AREA = 200000

COLOR_GREEN = (69, 200, 43)

CAM_ID = 2


# ----- FOREVER LOOP -----
# Generation of an captured object
WebCam = cv.VideoCapture(CAM_ID)

# Set resolution
WebCam.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
WebCam.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)


# repeat the following lines as long as the Webcam is accessible
while WebCam.isOpened():
    # Reading a single image from the WebCam
    Return, Image = WebCam.read()
    # Check whether image was captured
    if Return:

        PreProcessedPicture = pV.preProcessPicture(Image)
        ListOfContours = pV.findContours(PreProcessedPicture)
        CardFound, ListOfCardContours = pV.findCards(PreProcessedPicture, CARD_MIN_AREA, CARD_MAX_AREA)  # Picture, min area / max area

        cv.imshow("My Video", Image)
        cv.imshow("PreProcessedPicture", PreProcessedPicture)

        if CardFound:
            cv.drawContours(Image, ListOfContours, -1, COLOR_GREEN, 3)
            cv.drawContours(PreProcessedPicture, ListOfContours, -1, COLOR_GREEN, 3)







        if cv.waitKey(1) == ord('q'):
            break

# Close all windows
cv.destroyAllWindows()
