from tkinter import *
from PIL import ImageTk,Image,ImageDraw,ImageGrab
from tkinter import filedialog
from ImageModel import ImageModel

class Display:
    def __init__(self,methods,save_method,brush_methods):
        self.mode=0 #mode=0-draw, 1-create shape, 2-select, 3-transform
        self.shape=0 #shape 0-line,1-rectangle, 2-circle, 3-perspective
        #self.cursor_position = []  # x,y
        self.prev_position=[]
        self.clicked=[]
        self.methods=methods
        self.save_method=save_method
        self.brush=brush_methods
        self.root = Tk()
        self.root.title("Draw")
        self.root.geometry("1400x900")

        #top bar for buttons
        self.buttons_bar = LabelFrame(self.root)
        self.buttons_bar.place(x=0,y=0)


        self.frame = LabelFrame(self.root)
        self.frame.place(x=0,y=50)

        #workspace where the image is displayed
        self.workspace = LabelFrame(self.frame, padx=10,pady=10)
        self.workspace.grid(row=0, column=0)

        #layers of the image
        self.layers = LabelFrame(self.frame,padx=50)
        self.layers.grid(row=0, column=1)

        #add buttons to the button bar
        self.file_button = Button( self.buttons_bar , text="File", command=self.file_button_click)
        self.file_button.pack(side="left")
        #file buttons' drop down menu
        self.file_menu = Menu(self.root, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_chosen)
        self.file_menu.add_command(label="Open", command=self.open_chosen)
        self.file_menu.add_command(label="Save", command=self.save_chosen)
        self.file_menu.add_command(label="Save as...", command=self.save_as_chosen)

        self.draw_button = Button( self.buttons_bar , text="Draw",command=self.draw_button_click)
        self.draw_button.pack(side="left")

        self.shape_button = Button( self.buttons_bar , text="Shape",command=self.shape_button_click)
        self.shape_button.pack(side="left")
        #shape_button's drop down menu
        self.shape_menu = Menu(self.root, tearoff=0)
        self.shape_menu.add_command(label="Line",command=self.create_line)
        self.shape_menu.add_command(label="Rectangle", command=self.create_rectangle)
        self.shape_menu.add_command(label="Circle", command=self.create_circle)
        self.shape_menu.add_command(label="Perspective",command=self.create_perspective)

        self.size_button = Button(self.buttons_bar , text="Size",command=self.size_button_click)
        self.size_button.pack(side="left")
        #slider
        self.slider_frame=LabelFrame(self.root)
        self.size_slider=Scale(self.slider_frame,orient="horizontal",width=50, from_=1,to=100, command=self.get_slider_value)
        self.size_slider.grid(row=0, column=0)
        self.confirm_size=Button(self.slider_frame, text="X",command=self.hide_slider)
        self.confirm_size.grid(row=0, column=1)
        # colorpicker
        self.color_button = Button( self.buttons_bar , text="Color",command=self.color_button_click)
        self.color_button.pack(side="left")

        self.select_button = Button( self.buttons_bar , text="Select",command=self.select_button_click)
        self.select_button.pack(side="left")
        self.transform_button = Button( self.buttons_bar , text="Transform",command=self.transform_button_click)
        self.transform_button.pack(side="left")

        #scroll panes for the workspace
        self.h = Scrollbar(self.workspace, orient='horizontal')
        self.h.pack(side=BOTTOM, fill=X)
        self.v = Scrollbar(self.workspace)
        self.v.pack(side=RIGHT, fill=Y)

        #create canvas - only for displaying changes
        self.canvas = Canvas(self.workspace, bd=0, background="white", width=1000,height=800,xscrollcommand=self.h.set, yscrollcommand=self.v.set)
        self.canvas.pack(fill="both", expand=True)
        self.h.config(command=self.canvas.xview)
        self.v.config(command=self.canvas.yview)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        # mouse events
        self.canvas.bind("<Button-1>", self.left_click_action)
        self.canvas.bind("<B1-Motion>", self.hold_mouse_action)
        self.canvas.bind("<ButtonRelease-1>",self.release)


        #image for the canvas
        image = Image.new('RGBA', (1000, 1000), (250, 250, 250, 0))
        self.photo_image=ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)

        # placeholder for layers
        self.myLabel3 = Label(self.layers, text="Layers", padx=100)
        self.myLabel3.pack()



    def loop(self):

        self.root.mainloop()

    def file_button_click(self):

        self.file_menu.post(self.file_button.winfo_rootx(), self.file_button.winfo_rooty() + self.file_button.winfo_height())

    #creates new canvas
    def new_chosen(self):
        self.canvas.destroy()
        self.canvas = Canvas(self.workspace, bd=0, background="white", width=1000,height=800,xscrollcommand=self.h.set, yscrollcommand=self.v.set)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.canvas.pack(fill="both", expand=True)

    def open_chosen(self):#INVOLVE MODEL save path
        filename = filedialog.askopenfilename(initialdir="/gui/images", title="Open File",

                                                        filetypes=(("png", "*.png"), ("jpg", ".jpg"), ("any", "*.*")))

        if filename :
            self.model.image=Image.open(filename)
            self.photo_image = ImageTk.PhotoImage(self.model.image)
            w,h=self.model.image.size

            new_canvas = Canvas(self.workspace, width=w, height=h, xscrollcommand=self.h.set, yscrollcommand=self.v.set)
            self.h.config(command=new_canvas.xview)
            self.v.config(command=new_canvas.yview)

            new_canvas.create_image(0, 0, anchor=NW, image=self.background_image)

            self.canvas.destroy()

            self.canvas = new_canvas

            self.canvas.config(scrollregion=self.canvas.bbox(ALL))

            self.canvas.pack(fill="both", expand=True)



    def save_chosen(self):
        #get path from model
        pass
    def save_as_chosen(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")),
            title="Save Image As"
        )

        if file_path:
            self.save_method(file_path)



    def hold_mouse_action(self,event):
        if self.mode !=1:
            self.prev_position = self.clicked
            self.clicked = [event.x, event.y]

            self.methods.get(self.mode)([event.x,event.y,self.prev_position[0],self.prev_position[1]])
        #print("drag {0} {1} {2} {3}".format(event.x,event.y,self.prev_position[0],self.prev_position[1]))


    def left_click_action(self,event):
        #print("click")
        self.prev_position= [event.x, event.y]
        self.clicked = [event.x, event.y]
        if self.mode != 1:
            self.methods.get(self.mode)([event.x,event.y,self.prev_position[0],self.prev_position[1]])


    def release(self,event):
        #print("release")
        if self.mode !=0:
            x0=self.clicked[0]
            x1=event.x
            if event.x<x0:
                x1=x0
                x0=event.x

            y0=self.clicked[1]
            y1=event.y
            if event.y < y0:
                y1=y0
                y0 = event.y


            self.methods.get(self.mode)([self.shape,[x0,y0,x1,y1]])

    def draw_button_click(self):
        #enable drawing
        self.mode=0


    def shape_button_click(self):
        self.shape_menu.post(self.shape_button.winfo_rootx(),
                            self.shape_button.winfo_rooty() + self.shape_button.winfo_height())

    def create_line(self):
        self.mode=1
        self.shape=0
    def create_rectangle(self):
        self.mode = 1
        self.shape =1
    def create_circle(self):
        self.mode = 1
        self.shape=2
        
    def create_perspective(self):
        pass
    def size_button_click(self):
        self.slider_frame.place(x=self.size_button.winfo_x(),
                               y=self.size_button.winfo_y()+self.size_button.winfo_height())

    def get_slider_value(self,value):
        self.brush.get(0)(int(value))

    def hide_slider(self):
        self.slider_frame.place_forget()
    def color_button_click(self):
        print("hello")

    def select_button_click(self):
        print("hello")

    def transform_button_click(self):
        print("hello")




