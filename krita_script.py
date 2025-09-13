from krita import *
from PyQt5.QtWidgets import (QWidget, QAction)
import os
import xml.etree.ElementTree as ET
import random

'''
Adds random images from set as groups with paint layer to document
reference image transformed to fill half of screen
'''

class ImageSet:

    def __init__(self, image_path, name):
        # internal use
        self.document = Krita.instance().activeDocument()
        self.root_node = self.document.rootNode()

        self.name = name
        self.image = image_path
        self.group_node = self.addGroupNode()
        self.file_node = self.addFileNode()
        self.transform_node = self.addTransformNode()
        self.paint_node = self.addPaintNode()

        self.transform_node.setCollapsed(True)
        # resize and move image to right half of document
        self.fitRight()

        self.document.refreshProjection()
        self.document.setActiveNode(self.paint_node)

    def addGroupNode(self):
        node = self.document.createGroupLayer(self.name)
        self.root_node.addChildNode(node, None)

        return node 

    def addFileNode(self):
        node = self.document.createFileLayer('File Layer', self.image, None, None)
        self.group_node.addChildNode(node, None)

        return node

    def addPaintNode(self):
        node = self.document.createNode('Paint Layer', 'paintlayer')
        self.group_node.addChildNode(node, self.file_node)

        return node

    def addTransformNode(self):
        node = self.document.createTransformMask('Transform Mask')
        self.file_node.addChildNode(node, None)

        return node

    def getDocumentDimensions(self):
        width = self.document.width()
        height = self.document.height()

        return (width,height)

    def getImageDimensions(self):
        qrect = self.file_node.bounds()
        width = qrect.width()
        height = qrect.height()

        return (width,height)

    def getTargetParemeters(self):
        # returns list [x coordinate, y.coordinate, scale_ratio] to fit image on right half of screen
        document_dimensions = self.getDocumentDimensions()
        image_dimensions = self.getImageDimensions()
        max_size = (document_dimensions[0]/2, document_dimensions[1])
        
        # calculate scale ratio to fit half of document
        scale_ratio = 1
        # if width is greater, scale by width
        if image_dimensions[0] > image_dimensions[1]:
            scale_ratio = max_size[0]/image_dimensions[0]
        # else scale by height
        else:
            scale_ratio = max_size[1]/image_dimensions[1]

        # truncate decimal to avoid size escaping bounds by small amount
        scale_ratio = int(scale_ratio * 100) / 100

        scaled_image_size = (scale_ratio*image_dimensions[0],scale_ratio*image_dimensions[1])

        x_coordinate = int( ((document_dimensions[0]/2 - scaled_image_size[0]) // 2) + document_dimensions[0]/2 )
        y_coordinate = int( (document_dimensions[1] - scaled_image_size[1])//2 )

        return [x_coordinate, y_coordinate, scale_ratio] 

    def getTransformXML(self):
        return self.transform_node.toXML()

    def translate(self, x_coordinate, y_coordinate):
        # load and get xml string
        xml = self.getTransformXML()
        root = ET.fromstring(xml)

        # find and set coordinate values
        coordinates = root[1][0].find('transformedCenter')
        coordinates.set('x', str(x_coordinate))
        coordinates.set('y', str(y_coordinate))

        # create new xml string with modfied values
        new_xml = ET.tostring(root, encoding='unicode')
        # load xml to transform mask
        self.transform_node.fromXML(new_xml)
        self.document.refreshProjection()

    def scale(self, x_scale, y_scale):
        # load and get xml string
        xml = self.getTransformXML()
        root = ET.fromstring(xml)

        # find and set scale values 
        scale_x = root[1][0].find('scaleX')
        scale_x.set('value', str(x_scale))

        scale_y = root[1][0].find('scaleY')
        scale_y.set('value', str(y_scale))

        # create new xml string with modified values
        new_xml = ET.tostring(root, encoding='unicode')
        # load xml to transform mask
        self.transform_node.fromXML(new_xml)
        self.document.refreshProjection()

    def fitRight(self):
        # get [x,y,scale] to fit to right side of document
        target_parameters = self.getTargetParemeters()

        self.translate(target_parameters[0], target_parameters[1])
        self.scale(target_parameters[2], target_parameters[2])

    def hide(self):
        # hide entire group
        self.group_node.setVisible(False)
        self.document.refreshProjection()


def imageList(directory_path):
    # get list of all file names
    file_list = os.listdir(directory_path)
    
    # image suffixes to check
    suffixes = ('.png', '.jpg', '.jpeg')
    image_list = []
    for file in file_list:
        if file.endswith(suffixes):
            image_list.append(file)
    # return list of only images
    return image_list

def randomImage(directory_path):
    image_list = imageList(directory_path)

    return random.choice(image_list)

def newImageSet():
    # Directory for pool of images to be drawn from
    image_directory_path = ''
    image_name = randomImage(image_directory_path)
    name = image_name
    image_path = image_directory_path + '\\' + image_name

    # root_node = Krita.instance().activeDocument().rootNode()
    # child_nodes = root_node.childNodes()

    # # hide previous node very janky, but works for now
    # if len(child_nodes) > 2:
    #   child_nodes[len(child_nodes)-1].setVisible(False)
    #   Krita.instance().activeDocument().refreshProjection()

    image_set = ImageSet(image_path, name)


#create an action for group creation
extractAction = QAction("New image set")
extractAction.setShortcut("Ctrl+Tab")
extractAction.setStatusTip('New image set')
extractAction.triggered.connect(newImageSet)

# Create menu off main menu and add a new action to it
main_menu = Krita.instance().activeWindow().qwindow().menuBar()
custom_menu = main_menu.addMenu("Sets")
custom_menu.addAction(extractAction) # how to get items/actions in a menu

