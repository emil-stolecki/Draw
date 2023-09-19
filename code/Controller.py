from ImageModel import ImageModel
from Display import Display
from Brush import Brush
from Clipboard import Clipboard
from tkinter import *
from PIL import ImageTk,Image,ImageDraw
class Controller:
    ##

    def __init__(self):

        self.methods = {
            0: self.draw,
            1: self.create_shape(),
            2: self.select(),
            3: self.transform()
        }
        image = Image.new('RGBA', (1000, 1000), (250, 250, 250, 0))
        self.img = ImageModel("name", "path", image)
        self.brush=Brush(6,(0,0,0))
        self.clipBoard=Clipboard()
        self.display=Display(self.methods,self.save_image)



    def draw(self,x,y):
        #edit image
        draw = ImageDraw.Draw(self.img.image)
        draw.point((x,y),"black")
        #update display
        self.display.canvas.create_line(x,y,x+1,y+1)

    def create_shape(self):
        pass

    def select(self):
        pass
    def transform(self):
        pass

    def save_image(self,path):
        self.img.image.save(path)


