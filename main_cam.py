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

CARD_MIN_AREA = 59072
CARD_MAX_AREA = 72200

COLOR_GREEN = (69, 200, 43)
COLOR_BLUE = (255, 0, 0)

CAM_ID = 1


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
                cv.drawMarker(Image, (cX, cY), COLOR_BLUE)

            cv.drawContours(Image, ListOfCardContours, -1, COLOR_BLUE, 3)

            # Show SUIT and RANK in the same Window
            # Hori = np.concatenate((ListOfCards[0].suit_img, ListOfCards[0].rank_img), axis=1) # they dont have the same dimensions
            # cv.imshow("RANK / SUIT", Hori)


            # Just temp
            if len(ListOfCards) > 0:
                print(pV.identifyImage(ListOfCards[0].rank_img, True))
                print(pV.identifyImage(ListOfCards[0].suit_img, False))

                cv.imshow("Card 0", ListOfCards[i].img)
                cv.imshow("Suit 0", ListOfCards[i].suit_img)
                cv.imshow("Rank 0", ListOfCards[i].rank_img)
            else:
                cv.destroyWindow("Card 0")
                cv.destroyWindow("Suit 0")
                cv.destroyWindow("Rank 0")



        # Draw box on Live video
        cv.drawContours(Image, ListOfContours, -1, COLOR_GREEN, 3)
        # Show live Video
        cv.imshow("My Video", Image)

        if cv.waitKey(1) == ord('q'):
            break

# Close all windows
cv.destroyAllWindows()
