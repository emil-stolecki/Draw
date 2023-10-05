from tkinter import *
from PIL import ImageTk,Image,ImageDraw

class ImageModel:
    def __init__(self,name: str,path: str,image: Image):
        self.path = path
        self.image = image
        self.layers = []
        self.selected_piece=None


    def set_path(self,path: str):
        self.path=path

    def get_path(self):
        return self.path


    def get_image(self):
        return self.image


    def assign_selected(self, selected):
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

