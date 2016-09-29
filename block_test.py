#!/usr/bin/python
from __future__ import division



import cv2
import sys

import block
import blur
import color
import contour


def main(args=sys.argv):
    """
    Simple demo - reads an image, displays it, and writes it as 'foo.png'
    """
    if len(args) < 2:
        print "Usage: %s <img>" % (args[0])
        return

    reader = block.FileReader("Input", args[1])
    gray = color.BgrToGray("Gray", reader)
    blurred = blur.MedianBlur("Blur", gray)
    thresh = contour.AdaptiveThreshold("Thresh", blurred)
    contoured = contour.Contours("Contour", {'gray': gray, 'threshold': thresh})
    display = block.Display("Display", contoured)

    reader.load_params()
    reader.read()
    cv2.waitKey(0)
    reader.save_params()

if __name__=='__main__':
    main()
