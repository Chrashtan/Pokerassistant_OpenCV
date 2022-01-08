import cv2 as cv
import processVideo as pV

# Constants
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

CAM_ID = 1

cam = cv.VideoCapture(CAM_ID)

cam.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
print("When Card is found  press spacebar. To abort press ESC")

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    # Find Contour
    binFrame = pV.preProcessPicture(frame)
    cnt = pV.findContours(binFrame)
    cv.drawContours(frame, cnt, -1, (69, 200, 43), 3)
    cv.imshow("Calibration", frame)
    k = cv.waitKey(1)

    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        RoI = cv.selectROI('Please select ROI:', frame)
        x = RoI[0]  # x coordinate of top-left corner point of ROI
        y = RoI[1]  # y coordinate of top-left corner point of ROI
        w = RoI[2]  # Width of RoI
        h = RoI[3]  # Height of RoI
        # 7. ------------- Create my RoI Image ------------------
        RoIImage = frame[y:y + h, x:x + w]
        RoIBin = pV.preProcessPicture(RoIImage)
        RoIcnt = pV.findContours(RoIBin)

        # Uses the Card Area to calculate min and max Area for a Card
        cardArea = round(cv.contourArea(RoIcnt[0]))  # Card is biggest contour so at pos 0
        minArea = round(cardArea - (0.1 * cardArea))  # subract 10%
        maxArea = round(cardArea + (0.1 * cardArea))  # add 10%
        print("Contour Area: ", cardArea)
        print("Card min Area: ", minArea)
        print("Card max Area: ", maxArea)
        # ESC pressed
        print("Escape hit, closing...")
        break

cam.release()

cv.destroyAllWindows()
