# Poker Assistant with OpenCV
This script assist the player by playing poker. This only works for 2 Players, a webcam ist required. 
    
# Installation
Works on Python 3.8 with OpenCV.\
You need to install the following packages:\
$ **pip install poker**\
$ **conda install pandas**\
$ **pip install ipython** 

# How to use it
You need a camera with a top view on the board. The Background should be dark with fewer contours.
Works best for a plain black background. The lighting should be so that the cards don't reflect 
the light of the lamp. 
\
When you start the main_cam.py you should first calibrate the camera. To perform this press 'c' 
on your keyboard. A new window will open, there you should draw a RoI (Region of Interest) around 
a single card. The script will calculate an area to recognize a card. The algorithm to detect the
cards works fine, but if there is a different between the card and the binary compare image the 
script will detect a wrong card. The known errors are with the ranks "Five", "Six", "Nine",
"Ten" and "King" the script confuses the cards with each other. A workaround for that 
to edit the binary images of the cards with MC paint to match get better matches with the own deck.
After all ist set up you can play Cards with the following keybindings. 


# Keybindings 

**c** -> Calibration \
**h** -> Type in cards for the Hero \
**H** -> Detect cards of the Hero \
**f** -> Calculates odds for the FLOP \
**t** -> Calculates odds for the TURN \
**r** -> Calculates odds for the RIVER \
**w** -> Find winner

# References
Binary Images of the Cards (Modifided) from: https://github.com/EdjeElectronics/OpenCV-Playing-Card-Detector \
OpenCV: https://opencv.org/ \
Contour Features in OpenCV: https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html \
Poker Odds: https://github.com/souzatharsis/holdem_calc \



