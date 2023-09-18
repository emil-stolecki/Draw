from tkinter import *
from PIL import ImageTk,Image,ImageDraw

class ImageModel:
    def __init__(self,name: str,path: str,image: Image,size:int ,color:tuple):
        self.name = name
        self.path = path
        self.image = image
        self.brush_size = size
        self.brush_color = color
        self.selected_piece = None
        self.copied_piece = None
        self.layers = []



    def rename(self,name: str):
        self.name=name

    def set_path(self,path: str):
        self.path=path

    def set_image(self,image: Image):
        self.image=image

    def change_size(self,size:int):
         self.brush_size=size

    def change_color(self,color:tuple):
        self.brush_color=color

    def asign_selected(self,selected):
        self.selected_piece=selected

    def asign_copied(self,copied):
        self.copied_piece=copied

    def add_layer(self,layer:Image):
        self.layers.append(layer)

    def delete_layer(self,layer:Image):
        self.layers.remove(layer)

    def move_layer(self,layer:Image,direction: int):
        #0-down
        #1-up
         pass

    def copy_layer(self,layer:Image):
        pass

    def draw(self,layer:Image):
        pass

    def draw_shape(self,layer:Image):
        pass

    def apply_selected_location(self):
        pass

    def apply_selected_rotation(self):
        pass

    def apply_selected_scale(self):
        pass

    def save(self):
        pass
