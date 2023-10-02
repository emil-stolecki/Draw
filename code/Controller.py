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
            0:self._create_line,
            1:self._create_rectangle,
            2:self._create_circle,
            3:self._create_perspective,
            4:self._test
        }
        self.methods = {
            0: self.draw,
            1: self.create_shape,
            2: self.select,
            3: self.transform
        }

        image = Image.new('RGBA', (1000, 800), (255, 255, 255, 255))
        self.img = ImageModel(name="name", path=None, image=image)

        self.image_methods={
            0:self.save_image,
            1:self.img.set_path,
            2:self.img.get_path,
            3:self.new_image,
            4:self.img.get_image
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
        self.draw.ellipse((x1,y1,x2,y2),fill=self.brush.brush_color)
        self.draw.line((points[0], points[1], points[2], points[3]),width=self.brush.brush_size,fill=self.brush.brush_color)
        #update display
        self.display.canvas.create_oval(x1-0.5,y1-0.5,x2-0.5,y2-0.5,
                                        fill=self.brush.brush_color,outline="")
        self.display.canvas.create_line(points[0], points[1], points[2], points[3], width=self.brush.brush_size,fill=self.brush.brush_color)



    def create_shape(self, args):
        self.shapes.get(args[0])(args[1])#select method, pass arguments


    def _create_line(self,points):
        # edit image
        self.draw.line((points[0], points[1], points[2], points[3]),fill=self.brush.brush_color,width=self.brush.brush_size)
        #update_display
        self.display.canvas.create_line(points[0], points[1],
                                        points[2], points[3],
                                        fill=self.brush.brush_color,
                                        width=self.brush.brush_size)
    def _create_rectangle(self,points):
        size=self.brush.brush_size
        upper_correction=0
        lower_correction=0
        if size % 2 ==0:
            lower_correction = 1
        else:
            upper_correction = -1

        if self.brush.fill_color:
            # edit image
            self.draw.rectangle((points[0], points[1], points[2], points[3]),
                            outline=self.brush.brush_color,fill=self.brush.fill_color,width=size)

            # update display
            self.display.canvas.create_rectangle(points[0]+size/2+upper_correction, points[1]+size/2+upper_correction,
                                                 points[2]-size/2+lower_correction, points[3]-size/2+lower_correction,
                                                 outline=self.brush.brush_color, fill=self.brush.fill_color,
                                                 width=size)
        else:
            # edit image
            self.draw.rectangle((points[0], points[1], points[2], points[3]),
                                outline=self.brush.brush_color, width=size)
            # update display
            self.display.canvas.create_rectangle(points[0]+size/2+upper_correction, points[1]+size/2+upper_correction,
                                                 points[2]-size/2+lower_correction, points[3]-size/2+lower_correction,
                                                 outline=self.brush.brush_color,
                                                 width=size)

    def _create_circle(self,points):
        size = self.brush.brush_size
        correction = size/2
        is_same_point=False
        if points[0]==points[2] and points[1]==points[3]:
            is_same_point=True

        if is_same_point==False:#draw the cicle in a rectangle x1,y1,x2,y2
            if self.brush.fill_color:
                # edit image
                self.draw.ellipse((points[0], points[1], points[2], points[3]),
                              outline=self.brush.brush_color,fill=self.brush.fill_color, width=self.brush.brush_size)

                # update display
                self.display.canvas.create_oval(points[0]+correction, points[1]+correction,
                                            points[2]-correction, points[3]-correction,
                                            outline=self.brush.brush_color, fill=self.brush.fill_color,width=self.brush.brush_size)
            else:
                #edit image
                self.draw.ellipse((points[0], points[1], points[2], points[3]),
                          outline=self.brush.brush_color,width=self.brush.brush_size)
                #update display
                self.display.canvas.create_oval(points[0]+correction, points[1]+correction,
                                            points[2]-correction, points[3]-correction,
                                        outline=self.brush.brush_color,width=self.brush.brush_size)
        else:#draw the circle on the clicked point
            #edit image
            self.draw.ellipse((points[0]-correction, points[1]-correction,
                                    points[2]+correction, points[3]+correction),
                                  outline=self.brush.brush_color, fill=self.brush.brush_color,
                                  width=self.brush.brush_size)
            #update display
            self.display.canvas.create_oval(points[0], points[1],
                                            points[2], points[3],
                                            outline=self.brush.brush_color, fill=self.brush.brush_color,
                                            width=self.brush.brush_size)
    def _create_perspective(self):
        pass


    def select(self):
        pass
    def transform(self):
        pass

    def save_image(self,path):
        self.img.image.save(path)

    def new_image(self,image):
        self.img.image=image
        self.draw=ImageDraw.Draw(self.img.image)



    def _test(self,xd):
        w=51
        self.draw.ellipse((50, 50, 300, 300),
                          fill="pink", width=w)

        self.draw.ellipse((50, 50, 300, 300),
                          outline="black", width=1)

        # update display
        self.display.canvas.create_oval(50, 50, 300, 300,
                                        outline="", fill="pink", width=w)
        self.display.canvas.create_oval(50, 50, 300, 300,
                                        outline="black", width=1)