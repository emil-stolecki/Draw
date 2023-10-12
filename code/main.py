from tkinter import *
from PIL import ImageTk,Image,ImageDraw

from Controller import Controller

def main():

    c=Controller()
    c.display.loop()

if __name__ == "__main__":
    main()