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


# ----- FOREVER LOOP -----
# Generation of an captured object
WebCam = cv.VideoCapture(2) # 2 because of logitech capture

# Set resolution
cam.set(cv.CAP_PROP_FRAME_WIDTH, 1080)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)


# repeat the following lines as long as the Webcam is accessible
while WebCam.isOpened():
    # Reading a single image from the WebCam
    Return, Image = WebCam.read()
    # Check whether image was captured
    if Return:

        PreProcessedPicture = pV.preProcessPicture(Image)
        ListOfContours = pV.findContours(PreProcessedPicture)
        ListOfCardContours = pV.findCards(PreProcessedPicture, 100000, 200000)  # Picture, min area / max area

        cv.drawContours(Image, ListOfContours, -1, (69, 200, 43), 3)
        cv.drawContours(PreProcessedPicture, ListOfContours, -1, (69, 200, 43), 3)

        cv.imshow("My Video", Image)
        cv.imshow("PreProcessedPicture", PreProcessedPicture)





        if cv.waitKey(1) == ord('q'):
            break

# Close all windows
cv.destroyAllWindows()
