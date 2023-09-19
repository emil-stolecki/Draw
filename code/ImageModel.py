from tkinter import *
from PIL import ImageTk,Image,ImageDraw

class ImageModel:
    def __init__(self,name: str,path: str,image: Image):
        self.name = name
        self.path = path
        self.image = image
        self.layers = []
        self.selected_piece=None


    def rename(self,name: str):
        self.name=name

    def set_path(self,path: str):
        self.path=path

    def set_image(self,image: Image):
        self.image=image



    def asign_selected(self,selected):
        self.selected_piece=selected


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


