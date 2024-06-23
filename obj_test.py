from krita import *

application = Krita.instance()
current_document = application.activeDocument()

def get_current_layer():
    return current_document.activeNode()

def set_file_layer_image( file_layer_name, img_path, index = 0 ):
    # index  :  index of duplicate layer 
    file_layer = get_current_layer().parentNode().findChildNodes(file_layer_name)[index]
    file_layer.setProperties(img_path ,'' ,'')    

def add_file_layer(layer_name, img_path):
    file_layer = current_document.createNode(layer_name, 'filelayer')
    current_layer = get_current_layer()
    current_layer.parentNode().addChildNode(file_layer, current_layer)

    if img_path:
        set_file_layer_image(layer_name, img_path)

    return file_layer

def add_paint_layer(layer_name):
    new_layer = current_document.createNode(layer_name, 'paintlayer')
    current_layer = get_current_layer()
    current_layer.parentNode().addChildNode(new_layer, current_layer)

    return new_layer

def add_layer_set(paint_layer_name, file_layer_name, file_layer_img_path):
    # Add set of paint layer and file layer
    paint_layer = add_paint_layer(paint_layer_name)
    add_file_layer(file_layer_name, file_layer_img_path)
    
    current_document.setActiveNode(paint_layer)


sample_img = '/home/ningen/Pictures/dona-wallpaper.jpg'

"""
add_paint_layer('Paint Layer 3')
add_file_layer('Ref_3')
set_file_layer_image(sample_img, 'Ref_3')
application.action('activateNextLayer').trigger()
"""

add_layer_set('Paint Layer 2', 'Reference 2', sample_img)

#test
