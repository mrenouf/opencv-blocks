#!/usr/bin/python
from __future__ import division

import sys
import cv2


class Block(object):
    def __init__(self, name, sources={}):
        self.name = name
        self.image = None
        self.inputs = {}
        self.sources = {}
        self.outputs = {}
        self.params = {}
        self.param_window_name = 'p_' + name
        self.param_window_defined = False
        self.init_params()
        self.init_inputs()
        
        # support passing a raw block instance as 'default'
        if isinstance(sources, Block):
            sources = {'default': sources}

        self.sources = sources

        for input_name, child in sources.items():
            child.connect_to(self, input_name)
        
    def define_param(self, param_name, value, max_value, transform):
        if not self.param_window_defined:
            cv2.namedWindow(self.param_window_name, cv2.WINDOW_NORMAL)
            self.param_window_defined = True
            
        def onchange(f):
            self.params[param_name] = transform(f)
            print "[%s] %s = %f" % (self.name, param_name, self.params[param_name])

        cv2.createTrackbar(param_name, self.param_window_name, value, max_value, onchange)
        self.params[param_name] = transform(value)

    def define_input(self, name, desc):
        self.inputs[name] = {'name': name, 'description': desc }

    def init_params(self):
        pass

    def init_inputs(self):
        pass

    def param(self, name):
        return self.params[name]
    
    def input(self, name = 'default'):
        return self.sources[name].image
        
    def connect_to(self, child, input_name = 'default'):
        print "connect_to: %s %s" % (child, input_name)
        if not input_name in child.inputs:
            raise ValueError("child %s does not have an input '%s'" % (child.name, input_name))
        if self.outputs.has_key(child):
            raise ValueError("block %s is already connected to '%s' for input '%s'" % (self.name, child.name, input_name))
            
        # connect to child (for 'onchange/dispatch')
        self.outputs[child] = input_name
        # connect child to us (for 'get input')
        child.sources[input_name] = self
        print "Connected %s to %s (input %s)" % (self.name, child.name, input_name)
        return self

    def onchange(self, input_name=None):
        self.process(input_name)
        self.dispatch()

    def process(self, input_name):
        self.image = self.input(input_name).copy()

    def dispatch(self):
        for child, input_name in self.outputs.items():
            child.onchange(input_name)


class FileReader(Block):
    def __init__(self, name, filename):
        super(FileReader, self).__init__(name)
        self.filename = filename

    def read(self):
        self.onchange()
        
    def onchange(self):
        self.image = cv2.imread(self.filename)
        print "Read %s" % (self.filename)
        self.dispatch()


class FileWriter(Block):
    def __init__(self, name, filename, sources={}):
        super(FileWriter, self).__init__(name, sources)
        self.filename = filename

    def init_inputs(self):
        self.define_input('default', 'image to write')
    
    def process(self, input_name):
        cv2.imwrite(self.filename, self.sources[input_name].image)
        print "Wrote %s" % (self.filename)
        
    def read(self):
        self.onchange()
        

class Display(Block):
    def __init__(self, name, sources={}):
        super(Display, self).__init__(name, sources)
        self.window_name = name
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        #cv2.resizeWindow(self.window_name, 800, 480);    

    def init_inputs(self):
        self.define_input('default', 'image to display')
    
    def process(self, input_name=None):
        self.image = self.input()
        cv2.imshow(self.window_name, self.image)


def main(args=sys.argv):
    """
    Simple demo - reads an image, displays it, and writes it as 'foo.png'
    """
    if len(args) < 2:
        print "Usage: %s <img>" % (args[0])
        return

    reader = FileReader("Input", args[1])

    # connect a source to the input 'default' in the constructor
    display = Display("Display", reader)

    # explicitly define one or more input connections in constructor 
    writer = FileWriter("Writer", 'foo.png', {'default': reader})

    ## or connect after construction
    # display = Display("Display2")
    # reader.connect_to(display2)

    ## optionally specify the input name
    # reader.connect_to(display2, 'other')
    
    reader.read()
    cv2.waitKey(0)

if __name__=='__main__':
    main()
