'''
Contains all functions related to graphical display.

Created on Nov 19, 2011

@author: Julien Lengrand-Lambert
@email: julien@lengrand.fr
'''

import sys
import cv

def display_single_image(img, name="Image", x_pos=0, y_pos=0, delay=0):
    """
    Displays an image on screen.
    Position can be chosen, and time on screen too.
    Delay corresponds to the display time, in milliseconds.
    If delay =0, the Image stays on screen until user interaction.
    ----
    Ex:
    img = cv.LoadImage("../data/tippy.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
    display_single_image(img, "My Tippy", 0, 0, 100)
    """
    #TODO: Still not implemented!
    
    if not isinstance(name, str):
        raise TypeError("(%s) Name :String expected!" % (sys._getframe().f_code.co_name))
    if (not isinstance(x_pos, int)) \
        or (not isinstance(x_pos, int)) \
        or (not isinstance(x_pos, int)) :
            raise TypeError("(%s) Int expected!" % (sys._getframe().f_code.co_name))

    cv.StartWindowThread()
    cv.NamedWindow(name)
    cv.MoveWindow(name, x_pos, y_pos)
    cv.ShowImage(name, img)
    cv.WaitKey(delay)
    cv.DestroyWindow(name)