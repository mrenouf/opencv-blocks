#!/usr/bin/python
from __future__ import division

import sys
import cv2
import block

class GaussianBlur(block.Block):
    def __init__(self, name, source):
        super(GaussianBlur, self).__init__(name, source)

    def init_params(self):
        self.define_param('KSIZE_X', 5, 33,
                lambda f: max(0, (f * 2) - 1),
                lambda f: round(f / 2))
        self.define_param('KSIZE_Y', 5, 33,
                lambda f: max(0, (f * 2) - 1),
                lambda f: round(f / 2))
        self.define_param('SIGMA_X', 10, 1000,
                lambda f: float(max(1, f/10)),
                lambda f: f * 10)
        self.define_param('SIGMA_Y', 10, 1000,
                lambda f: float(max(1, f/10)),
                lambda f: f * 10)

    def init_inputs(self):
        self.define_input('default', 'image to blur')

    def process(self, input_name = "default"):
        self.image = cv2.GaussianBlur(
            self.input().copy(),
            (self.param('KSIZE_X'), self.param('KSIZE_Y')),
            self.param('SIGMA_X'),
            None,
            self.param('SIGMA_Y'))


class MedianBlur(block.Block):
    def __init__(self, name, source):
        super(MedianBlur, self).__init__(name, source)

    def init_params(self):
        self.define_param('APERATURE', 5, 33,
                lambda f: max(3, (f * 2) - 1),
                lambda f: int(round(f / 2)))

    def init_inputs(self):
        self.define_input('default', 'image to blur')

    def process(self, input_name = "default"):
        self.image = cv2.medianBlur(self.input(), self.param('APERATURE'))

