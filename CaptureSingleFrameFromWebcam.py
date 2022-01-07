import cv2 as cv
import processVideo as pV



# Constants
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

CAM_ID = 2

cam = cv.VideoCapture(CAM_ID)

cam.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

cv.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    # Find Contour
    binFrame = pV.preProcessPicture(frame)
    cnt = pV.findContours(binFrame)
    cv.drawContours(frame, cnt, -1, (69, 200, 43), 3)
    cv.imshow("test", frame)

    k = cv.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        cardArea = round(cv.contourArea(cnt[0]))   # Card is biggest contour so at pos 0
        minArea = round(cardArea - (0.1*cardArea))  # subract 10%
        maxArea = round(cardArea + (0.1*cardArea))  # add 10%
        print("Contour Area: ", cardArea)
        print("Card min Area: ", minArea)
        print("Card max Area: ", maxArea)
        # ESC pressed
        print("Escape hit, closing...")
        break


cam.release()

cv.destroyAllWindows()