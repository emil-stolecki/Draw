from tkinter import *
from PIL import ImageTk,Image,ImageDraw,ImageGrab
from tkinter import filedialog
from ImageModel import ImageModel

class Display:
    def __init__(self,methods,save_method):
        self.mode=0 #mode=0-draw, 1-create shape, 2-select, 3-transform
        self.cursor_position = []  # x,y
        self.methods=methods
        self.save_method=save_method
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
        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="New", command=self.new_chosen)
        self.menu.add_command(label="Open", command=self.open_chosen)
        self.menu.add_command(label="Save", command=self.save_chosen)
        self.menu.add_command(label="Save as...", command=self.save_as_chosen)

        self.draw_button = Button( self.buttons_bar , text="Draw",command=self.draw_button_click)
        self.draw_button.pack(side="left")

        self.shape_button = Button( self.buttons_bar , text="Shape",command=self.shape_button_click)
        self.shape_button.pack(side="left")
        self.size_button = Button( self.buttons_bar , text="Size",command=self.size_button_click)
        self.size_button.pack(side="left")
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

        self.menu.post(self.file_button.winfo_rootx(), self.file_button.winfo_rooty() + self.file_button.winfo_height())

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
        self.cursor_position=[event.x,event.y]
        self.methods.get(self.mode)(event.x,event.y)


    def left_click_action(self,event):
        self.cursor_position=[event.x, event.y]




    def draw_button_click(self):
        #enable drawing
        self.mode=0

        #instead of booleans, one int

        #ImageDraw.point(xy, fill=None)
        #canvas.bind("<Button-1>", get_x_and_y)
        #canvas.bind("<B1-Motion>", draw_smth)


        #img = Image.new('RGBA', (500, 500), (250, 250, 250,0))
        #draw = ImageDraw.Draw(img)
        #rectangle_coords = [(50, 50), (450, 250)]
        #rectangle_color = (255, 0, 0)

        #draw.rectangle(rectangle_coords, fill=rectangle_color)
        #for the display
        #self.photo_image.paste(img)
        #actual edit
        #self.model.image.paste(img)

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




