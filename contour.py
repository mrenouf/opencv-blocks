#!/usr/bin/python
from __future__ import division


import numpy as np
import cv2

import block


class AdaptiveThreshold(block.Block):
    def __init__(self, name,  sources={}):
        super(AdaptiveThreshold, self).__init__(name, sources)

    def init_params(self):
        self.define_param('BLOCK_SIZE', 21, 101,
                lambda f: max(3, (f * 2) - 1),
                lambda f: int(round(f / 2)))
        self.define_param('C', 20, 101,
                lambda f: max(3, (f * 2) - 1),
                lambda f: int(round(f / 2)))

    def init_inputs(self):
        self.define_input('default', 'Single channel (gray) image')

    def process(self, input_name="default"):
        self.image = cv2.adaptiveThreshold(
            self.input(), 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            self.param('BLOCK_SIZE'),
            self.param('C'))


class Contours(block.Block):
    def __init__(self, name, sources={}):
        super(Contours, self).__init__(name, sources)

    def init_inputs(self):
        self.define_input('gray', 'Single channel gray image')
        self.define_input('threshold', 'Single channel threshold image')

    def process(self, input_name="default"):
        #if input_name == "threshold":
        self.contours, hierarchy = cv2.findContours(self.input("threshold"),
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        #if input_name == "gray":
        self.image = self.input("gray").copy()
        self.image = (self.image * 0.3).astype(np.uint8)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(self.image, self.contours, -1, (0, 255, 0))

