class Brush:
    def __init__(self,size ,color):
        self.brush_size = size
        if type(color)==tuple:
            self.brush_color = "#%02x%02x%02x" % color
        if type(color)==str:
            self.brush_color = color
        self.fill_color=None

    def change_size(self,size:int):
         self.brush_size=size

    def change_color(self,color:tuple):
        self.brush_color=color

    def change_fill(self,color:tuple):
        self.fill_color=color

    def get_size(self):
        return self.brush_size

    def remove_fill(self):
        self.fill_color=None