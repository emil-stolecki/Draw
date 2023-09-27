from ImageModel import ImageModel
from Display import Display
from Brush import Brush
from Clipboard import Clipboard
from tkinter import *
from PIL import ImageTk,Image,ImageDraw
class Controller:
    ##

    def __init__(self):
        self.shapes ={
            0:self.create_line,
            1:self.create_rectangle,
            2:self.create_circle,
            3:self.create_perspective
        }
        self.methods = {
            0: self.draw,
            1: self.create_shape,
            2: self.select,
            3: self.transform
        }

        image = Image.new('RGBA', (1000, 1000), (250, 250, 250, 100))
        self.img = ImageModel("name", "path", image)
        self.brush=Brush(6,(0,0,0))

        self.brush_methods= {
            0:self.brush.change_size,
            1:self.brush.change_color,
            2:self.brush.change_fill
        }
        self.clipBoard=Clipboard()
        self.display=Display(self.methods,self.save_image,self.brush_methods)

        self.draw = ImageDraw.Draw(self.img.image)

    def draw(self,points):
        x1,x2=points[0]-self.brush.brush_size/2,points[0]+self.brush.brush_size/2
        y1,y2=points[1]-self.brush.brush_size/2,points[1]+self.brush.brush_size/2
        #edit image
        self.draw.ellipse((x1,y1,x2,y2),fill=self.brush.brush_color)
        self.draw.line((points[0], points[1], points[2], points[3]),width=self.brush.brush_size,fill=self.brush.brush_color)
        #update display
        self.display.canvas.create_oval(x1,y1,x2,y2, fill=self.brush.brush_color)
        self.display.canvas.create_line(points[0], points[1], points[2], points[3], width=self.brush.brush_size,fill=self.brush.brush_color)


    def create_shape(self, args):
        self.shapes.get(args[0])(args[1])


    def create_line(self,points):
        # edit image
        self.draw.line((points[0], points[1], points[2], points[3]),fill=self.brush.brush_color,width=self.brush.brush_size)
        #update_display
        self.display.canvas.create_line(points[0], points[1], points[2], points[3],fill=self.brush.brush_color,width=self.brush.brush_size)
    def create_rectangle(self,points):

        if self.brush.fill_color:
            # edit image
            self.draw.rectangle((points[0], points[1], points[2], points[3]),
                            outline=self.brush.brush_color,fill=self.brush.fill_color,width=self.brush.brush_size)

            # update display
            self.display.canvas.create_rectangle(points[0], points[1], points[2], points[3],
                                                 outline=self.brush.brush_color, fill=self.brush.fill_color,
                                                 width=self.brush.brush_size)
        else:
            # edit image
            self.draw.rectangle((points[0], points[1], points[2], points[3]),
                                outline=self.brush.brush_color, width=self.brush.brush_size)
            # update display
            self.display.canvas.create_rectangle(points[0], points[1], points[2], points[3],
                                                 outline=self.brush.brush_color,
                                                 width=self.brush.brush_size)

    def create_circle(self,points):
        if self.brush.fill_color:
            # edit image
            self.draw.ellipse((points[0], points[1], points[2], points[3]),
                              outline=self.brush.brush_color,fill=self.brush.fill_color, width=self.brush.brush_size)
            # update display
            self.display.canvas.create_oval(points[0], points[1], points[2], points[3],
                                            outline=self.brush.brush_color, fill=self.brush.fill_color,width=self.brush.brush_size)
        else:
            #edit image
            self.draw.ellipse((points[0], points[1], points[2], points[3]),
                          outline=self.brush.brush_color,width=self.brush.brush_size)
            #update display
            self.display.canvas.create_oval(points[0], points[1], points[2], points[3],
                                        outline=self.brush.brush_color,width=self.brush.brush_size)
    def create_perspective(self):
        pass


    def select(self):
        pass
    def transform(self):
        pass

    def save_image(self,path):
        self.img.image.save(path)


