from krita import *
from PyQt5.QtWidgets import (QWidget, QAction)
import os, random

class Layer:
    def __init__(self, layer_type, layer_name):
        self.type = layer_type
        self.name = layer_name
        self.current_document = Krita.instance().activeDocument()
        match layer_type:
            case 'paintlayer':
                self.node = self.current_document.createNode(layer_name, layer_type)
            case 'filelayer':
                self.node = self.current_document.createFileLayer(layer_name, '', '', '')

    def get_current_layer(self):
        return self.current_document.activeNode()

    def add_layer_to_document(self):
        current_layer = self.get_current_layer()
        current_layer.parentNode().addChildNode(self.node, current_layer)

    def set_file_layer_image(self, img_path):
        if self.type == 'filelayer':
            self.node.setProperties(img_path, '', '')

    def refresh_projection(self):
        self.current_document.refreshProjection()

    def hide(self):
        self.node.setVisible(False)
        self.refresh_projection()

    def show(self):
        self.node.setVisible(True)
        self.refresh_projection()

    def set_active(self):
        '''
        set node as actively selected layer
        does not work as expected or at all not necessary for initial trial 
        currently relying on order of layer creation/adding for selection of layers
        '''
        self.current_document.setActiveNode(self.node)


class Set:
    
    def __init__(self, name, image_path):
        self.file_layer = Layer('filelayer', 'Ref Layer ' + str(name))
        self.file_layer.add_layer_to_document()
        self.file_layer.set_file_layer_image(image_path)
        self.paint_layer = Layer('paintlayer', 'Paint Layer ' + str(name))
        self.paint_layer.add_layer_to_document()
        self.name = name

    def add_set_to_document(self):
        self.file_layer.add_layer_to_document()
        self.paint_layer.add_layer_to_document() 

    def hide(self):
        self.file_layer.hide()
        self.paint_layer.hide()

    def show(self):
        self.file_layer.show()
        self.paint_layer.show()


class Session:

    def __init__(self):
        self.timer = 0
        self.count = 0
        self.sets = []
        self.image_list = []
        self.index = -1
        self.source = '/home/ningen/images/'
        
    def set_source(self, source):
        self.source = source

    def start(self, count = 10, timer = 60, source = '/home/ningen/images/'):
        self.timer = timer
        self.count = count
        self.source = source
        self.prepare_list()
        
    def next(self):
        if self.index > -1:
            self.sets[self.index].hide()
            
        self.index = self.index + 1
        self.sets.append( Set(self.index+2, self.source+self.image_list[self.index]) )
        
    def prepare_list(self):
        self.image_list = os.listdir(self.source)
        
        # Not good but works for test. need to cut off at count to avoid pointless looping
        for x in range(len(self.image_list)):
            rand = random.randrange(len(self.image_list))
            self.image_list[x], self.image_list[rand] = self.image_list[rand], self.image_list[x]

        if self.count > len(self.image_list):
            self.count = len(self.image_list)

        self.image_list = self.image_list[:self.count]


def test_function():
    x = Set('2', sample_img)
    return 'test_function return'

sample_img = '/home/ningen/images/sample.jpg'

"""
x = Layer('filelayer', 'Ref Layer 2')
print(x.type, x.name)
x.add_layer_to_document()
x.set_file_layer_image(sample_img)
"""

"""
f = Layer('filelayer', 'Ref Layer 2')
f.add_layer_to_document()
f.set_file_layer_image(sample_img)

p = Layer('paintlayer', 'Paint Layer 2')
p.add_layer_to_document()
"""
"""
x = Set('2', sample_img)
"""


session = Session()
session.start(source='/home/ningen/images/dona/')
print(session.image_list)

#create an action that does stuff
extractAction = QAction("next")
extractAction.setShortcut("Ctrl+`")
extractAction.setStatusTip('Next image')
extractAction.triggered.connect(session.next)

# Create menu off main menu and add a new action to it
main_menu = Krita.instance().activeWindow().qwindow().menuBar()
custom_menu = main_menu.addMenu("gesture")
custom_menu.addAction(extractAction) # how to get items/actions in a menu

