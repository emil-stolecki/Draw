class Brush:
    def __init__(self,size:int ,color:tuple):
        self.brush_size = size
        self.brush_color = color

    def change_size(self,size:int):
         self.brush_size=size

    def change_color(self,color:tuple):
        self.brush_color=color