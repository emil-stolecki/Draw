from tkinter import *
from PIL import ImageTk,Image,ImageDraw

class View:
    def __init__(self):
        self.root = Tk()
        self.root.title("Draw")
        self.root.geometry("800x600")


        self.buttons_bar = LabelFrame(self.root)
        self.buttons_bar.place(x=0,y=0)


        self.frame = LabelFrame(self.root)
        self.frame.place(x=0,y=50)

        self.workspace = LabelFrame(self.frame, padx=10,pady=10)
        self.workspace.grid(row=0, column=0)
        self.layers = LabelFrame(self.frame,padx=50)
        self.layers.grid(row=0, column=1)

        button_holder = LabelFrame(self.buttons_bar)
        button_holder.pack(side="left")


        self.file_button = Button(button_holder, text="File", command=self.file_button_click).pack(side="left")
        self.draw_button = Button(button_holder, text="Draw",command=self.draw_button_click).pack(side="left")
        self.shape_button = Button(button_holder, text="Shape",command=self.shape_button_click).pack(side="left")
        self.size_button = Button(button_holder, text="Size",command=self.size_button_click).pack(side="left")
        self.color_button = Button(button_holder, text="Color",command=self.color_button_click).pack(side="left")
        self.select_button = Button(button_holder, text="Select",command=self.select_button_click).pack(side="left")
        self.transform_button = Button(button_holder, text="Transform",command=self.transform_button_click).pack(side="left")

        self.myLabel2 = Label(self.workspace, text="Workspace", padx=100)
        self.myLabel3 = Label(self.layers, text="Layers",padx=100)


        empty_img = Image.new('RGB', (500, 500), (255, 255, 255))
        self.empty_img_photo = ImageTk.PhotoImage(empty_img)

        self.empty_img_label = Label(self.workspace,image=self.empty_img_photo)
        self.empty_img_label.image=self.empty_img_photo

        self.empty_img_label.pack()

        self.myLabel3.pack()



    def loop(self):
        self.root.mainloop()

    def donothing(self):
        print("jjjj")
    def file_button_click(self):
        img = Image.new('RGB', (600, 600), (255, 255, 0))
        iii = ImageTk.PhotoImage(img)
        self.empty_img_label.config(image=iii)
        self.empty_img_label.image=iii
        return "ok"

    def draw_button_click(self):
        print("hello")

    def shape_button_click(self):
        print("hello")

    def size_button_click(self):
        print("hello")

    def color_button_click(self):
        print("hello")

    def select_button_click(self):
        print("hello")

    def transform_button_click(self):
        print("hello")




