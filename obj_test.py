from krita import *


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
        self.file_layer = Layer('filelayer', 'Ref Layer ' + name)
        self.file_layer.add_layer_to_document()
        self.file_layer.set_file_layer_image(image_path)
        self.paint_layer = Layer('paintlayer', 'Paint Layer ' + name)
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

    DEFAULT_SOURCE = '/home/ningen/Pictures/'

    def __init__(self, timer, count):
        self.timer = timer
        self.count = count
        self.sets = []
        self.index = 0

    #def start():
            

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

