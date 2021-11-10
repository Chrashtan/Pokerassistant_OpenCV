# Import OpenCV Library
import cv2 as cv
# Generation of an captured object
WebCam = cv.VideoCapture(1)

# repeat the following lines as long as the Webcam is accessible
while WebCam.isOpened():
    # Reading a single image from the WebCam
    Return, Image = WebCam.read()
    # Check whether image was captured
    if Return:
        # Change the size of the image
        ChangedImage = cv.resize(Image, dsize=(0, 0), fx=0.5, fy=0.5)

        # Convert the webcam image from BGR to HSV color space
        Image_hsv = cv.cvtColor(Image, cv.COLOR_BGR2HSV)

        # Convert the webcam image from BGR to HSV color space
        Image_GRAY = cv.cvtColor(Image, cv.COLOR_BGR2GRAY)

        # Show the contents of image
        cv.imshow('WebCam', Image)
        cv.imshow('B', ChangedImage[:, :, 0])
        cv.imshow('G', ChangedImage[:, :, 1])
        cv.imshow('R', ChangedImage[:, :, 2])
        if cv.waitKey(1) == ord('q'):
            break

# Close all windows
cv.destroyAllWindows()
