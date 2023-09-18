from tkinter import *
from PIL import ImageTk,Image,ImageDraw

from ImageModel import ImageModel
from View import View
def main():

    view=View()


    img = Image.new('RGB', (500, 500), (250, 250, 250))  # mone, h-w, bg color
    a=ImageModel("name","path",img,5,(0,0,0))



    view.loop()

if __name__ == "__main__":
    main()