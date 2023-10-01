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
            1: self.erase,
            2: self.create_shape,
            3: self.select,
            4: self.transform
        }

        image = Image.new('RGBA', (1000, 800), (255, 255, 255, 255))
        self.img = ImageModel(name="name", path=None, image=image)

        self.image_methods={
            0:self.save_image,
            1:self.img.set_path,
            2:self.img.get_path,
            3:self.new_image
        }
        self.brush=Brush(6,(0,0,0))

        self.brush_methods= {
            0:self.brush.change_size,
            1:self.brush.change_color,
            2:self.brush.change_fill,
            3:self.brush.get_size,
            4:self.brush.remove_fill
        }
        self.clipBoard=Clipboard()
        self.display=Display(self.methods,self.image_methods,self.brush_methods)

        self.draw = ImageDraw.Draw(self.img.image)

    def draw(self,points):
        x1,x2=points[0]-self.brush.brush_size/2,points[0]+self.brush.brush_size/2
        y1,y2=points[1]-self.brush.brush_size/2,points[1]+self.brush.brush_size/2
        #edit image
        self.draw.ellipse((x1,y1,x2,y2),fill=self.brush.brush_color,outline=self.brush.brush_color)
        self.draw.line((points[0], points[1], points[2], points[3]),width=self.brush.brush_size,fill=self.brush.brush_color)
        #update display
        self.display.canvas.create_oval(x1,y1,x2,y2, fill=self.brush.brush_color,outline=self.brush.brush_color)
        self.display.canvas.create_line(points[0], points[1], points[2], points[3], width=self.brush.brush_size,fill=self.brush.brush_color)


    #CANT EREASE
    def erase(self,points):
        x1, x2 = points[0] - self.brush.brush_size / 2, points[0] + self.brush.brush_size / 2
        y1, y2 = points[1] - self.brush.brush_size / 2, points[1] + self.brush.brush_size / 2
        # edit image
        self.draw.ellipse((x1, y1, x2, y2), fill=self.brush.fill_color, outline=self.brush.fill_color)
        self.draw.line((points[0], points[1], points[2], points[3]), width=self.brush.brush_size,
                       fill=self.brush.fill_color)
        # update display
        self.display.canvas.create_oval(x1, y1, x2, y2, fill=self.brush.fill_color, outline=self.brush.fill_color)
        self.display.canvas.create_line(points[0], points[1], points[2], points[3], width=self.brush.brush_size,
                                        fill=self.brush.fill_color)
    def create_shape(self, args):
        self.shapes.get(args[0])(args[1])#select method, pass arguments


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

    def new_image(self,image):
        self.img = ImageModel(name="name", path=None, image=image)
        self.draw=ImageDraw.Draw(self.img.image)


