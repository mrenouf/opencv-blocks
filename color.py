#!/usr/bin/python

import cv2
import block


class BgrToGray(block.Block):
    def __init__(self, source, name):
        super(BgrToGray, self).__init__(source, name)

    def init_inputs(self):
        self.define_input('default', 'Color 3 channel (BGR) image')

    def process(self, input_name):
        self.image = cv2.cvtColor(self.input(), cv2.COLOR_BGR2GRAY)

