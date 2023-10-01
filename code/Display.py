from tkinter import *
from PIL import ImageTk,Image,ImageDraw,ImageGrab
from tkinter import filedialog,colorchooser
from ImageModel import ImageModel

class Display:
    def __init__(self,methods,image_method,brush_methods):
        self.mode=0 #mode=0-draw,1-erease,2-create shape 3-select, 4-transform
        self.shape=0 #shape 0-line,1-rectangle, 2-circle, 3-perspective
        #self.cursor_position = []  # x,y
        self.prev_position=[]
        self.clicked=[]
        self.methods=methods
        self.image_method=image_method
        self.brush=brush_methods
        self.root = Tk()
        self.root.title("Draw")
        self.root.geometry("1400x900")

        self.theme={
            "main_color" : "#7f7f7f",
            "button":"#c3c3c3",
            "button_border":"#616161",
            "button_active":"#f4f4f4",
            "layers_tab": "#6b6b6b",
            "l_buttons":"#7f7f7f",
            "l+button_border":"#616161"
        }
        self.root.configure(background=self.theme.get("main_color"))
        #top bar for buttons
        self.buttons_bar = Frame(self.root,bg=self.theme.get("main_color"))
        self.buttons_bar.place(x=0,y=0)


        self.frame = LabelFrame(self.root,bg=self.theme.get("main_color"))
        self.frame.place(x=0,y=50)

        #workspace where the image is displayed
        self.workspace = LabelFrame(self.frame, padx=10,pady=10,bg=self.theme.get("main_color"))
        self.workspace.grid(row=0, column=0)

        #layers of the image
        self.layers = LabelFrame(self.frame,padx=50,bg=self.theme.get("layers_tab"))
        self.layers.grid(row=0, column=1)

        #add buttons to the button bar
        self.file_button = Button( self.buttons_bar , text="File", command=self.file_button_click,height=2,width=5,bg=self.theme.get("button"))
        self.file_button.pack(side="left")
        #file buttons' drop down menu
        self.file_menu = Menu(self.root, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_chosen)
        self.file_menu.add_command(label="Open", command=self.open_chosen)
        self.file_menu.add_command(label="Save", command=self.save_chosen)
        self.file_menu.add_command(label="Save as...", command=self.save_as_chosen)

        self.draw_button = Button( self.buttons_bar , text="Draw",command=self.draw_button_click,height=2,width=5,bg=self.theme.get("button_active"))
        self.draw_button.pack(side="left")
        # eraser
        self.erase_button = Button(self.buttons_bar, text="Erase", command=self.erase_button_click, height=2, width=5,bg=self.theme.get("button"))
        self.erase_button.pack(side="left")
        #shape_button
        self.shape_button = Button( self.buttons_bar , text="Shape",command=self.shape_button_click,height=2,width=5,bg=self.theme.get("button"))
        self.shape_button.pack(side="left")
        #shape_button's drop down menu
        self.shape_menu = Menu(self.root, tearoff=0)
        self.shape_menu.add_command(label="Line",command=self.create_line)
        self.shape_menu.add_command(label="Rectangle", command=self.create_rectangle)
        self.shape_menu.add_command(label="Circle", command=self.create_circle)
        self.shape_menu.add_command(label="Perspective",command=self.create_perspective)

        #brush size button
        self.size_button_frame_border=Frame(self.buttons_bar,padx=2,pady=2,bg=self.theme.get("button_border"))
        self.size_button_frame = Frame(self.size_button_frame_border,padx=8,bg=self.theme.get("button"))
        self.size_button_frame.pack()

        size_label = Label(self.size_button_frame, text="Size",bg=self.theme.get("button"))
        size_label.pack()
        self.size_ind = Label(self.size_button_frame, text="6",bg=self.theme.get("button"))
        self.size_ind.pack()

        self.size_button_frame.bind("<Button-1>", self.size_button_click)
        size_label.bind("<Button-1>", self.size_button_click)
        self.size_ind.bind("<Button-1>", self.size_button_click)

        self.size_button_frame_border.pack(side="left")
        #slider
        self.slider_frame=LabelFrame(self.root)
        self.size_slider=Scale(self.slider_frame,orient="horizontal",width=15, from_=1,to=100, command=self.get_slider_value)
        self.size_slider.grid(row=0, column=0)
        self.confirm_size=Button(self.slider_frame, text="X",command=self.hide_slider)
        self.confirm_size.grid(row=0, column=1)

        # brush color
        self.fg_color_frame_border = Frame(self.buttons_bar, padx=2, pady=2,bg=self.theme.get("button_border"))
        self.fg_color_frame = Frame(self.fg_color_frame_border, padx=3,bg=self.theme.get("button"))
        self.fg_color_frame.pack()

        fg_name_label = Label(self.fg_color_frame, text="Brush",bg=self.theme.get("button"))
        fg_name_label.pack()

        self.fg_color_image = Image.new('RGB', (35, 17), (0, 0, 0))
        self.fg_photo = ImageTk.PhotoImage(self.fg_color_image)
        self.fg_color = Label(self.fg_color_frame, image=self.fg_photo,bg=self.theme.get("button"))
        self.fg_color.pack()

        self.fg_color_frame.bind("<Button-1>", self.color_button_click)
        fg_name_label.bind("<Button-1>", self.color_button_click)
        self.fg_color.bind("<Button-1>", self.color_button_click)

        self.fg_color_frame_border.pack(side="left")

        # fill color
        self.bg_color_frame_border = Frame(self.buttons_bar, padx=2, pady=2,bg=self.theme.get("button_border"))
        self.bg_color_frame = Frame(self.bg_color_frame_border, padx=3,bg=self.theme.get("button"))
        self.bg_color_frame.pack()

        bg_name_label = Label( self.bg_color_frame, text="Fill",bg=self.theme.get("button"))
        bg_name_label.pack()

        self.bg_color_image = Image.new('RGBA', (35, 17), (255, 255, 255,0))
        self.bg_photo = ImageTk.PhotoImage(self.bg_color_image)
        self.bg_color = Label(self.bg_color_frame, image=self.bg_photo,bg=self.theme.get("button"))
        self.bg_color.pack()

        self.bg_color_frame.bind("<Button-1>",self.fill_button_click)
        bg_name_label.bind("<Button-1>", self.fill_button_click)
        self.bg_color.bind("<Button-1>", self.fill_button_click)

        self.bg_color_frame_border.pack(side="left")

        #remove fill
        self.remove_fill_button = Button(self.buttons_bar , text="No Fill",command=self.remove_fill_click,height=2,width=5,bg=self.theme.get("button"))
        self.remove_fill_button.pack(side="left")

        self.select_button = Button(self.buttons_bar , text="Select",command=self.select_button_click,height=2,width=5,bg=self.theme.get("button"))
        self.select_button.pack(side="left")
        self.transform_button = Button( self.buttons_bar , text="Transform",command=self.transform_button_click,height=2,width=5,bg=self.theme.get("button"))
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
        self.image_w=1000
        self.image_h=800
        image = Image.new('RGBA', (1000, 800), (255, 255, 255, 0))
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
        #create new image
        image = Image.new('RGBA', (1000,800), (60, 255, 255, 0))
        self.image_method.get(3)(image)#attach new image
        #create  new display
        self.canvas.destroy()
        self.canvas = Canvas(self.workspace, bd=0, background="white", width=1000,height=800,xscrollcommand=self.h.set, yscrollcommand=self.v.set)
        self.photo_image = ImageTk.PhotoImage(image)
        self.h.config(command=self.canvas.xview)
        self.v.config(command=self.canvas.yview)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.left_click_action)
        self.canvas.bind("<B1-Motion>", self.hold_mouse_action)
        self.canvas.bind("<ButtonRelease-1>", self.release)

    def open_chosen(self):
        filepath = filedialog.askopenfilename(initialdir="/gui/images", title="Open File",

                                                        filetypes=(("png", "*.png"), ("jpg", ".jpg"), ("any", "*.*")))

        if filepath:
            # create new image
            image = Image.open(filepath)
            self.image_method.get(3)(image)  # attach new image
            self.image_method.get(1)(filepath) #set path
            #create new display
            self.canvas.destroy()
            self.image_w , self.image_h=image.size
            self.canvas = new_canvas = Canvas(self.workspace, width=1000, height=800, xscrollcommand=self.h.set, yscrollcommand=self.v.set)
            self.photo_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
            self.h.config(command=self.canvas.xview)
            self.v.config(command=self.canvas.yview)
            self.canvas.config(scrollregion=self.canvas.bbox(ALL))
            self.canvas.pack(fill="both", expand=True)
            self.canvas.bind("<Button-1>", self.left_click_action)
            self.canvas.bind("<B1-Motion>", self.hold_mouse_action)
            self.canvas.bind("<ButtonRelease-1>", self.release)

    def save_chosen(self):
        if self.image_method.get(2)():#check if path exists
            self.image_method.get(0)(self.image_method.get(2)())#save
        else:
            self.save_as_chosen()
    def save_as_chosen(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")),
            title="Save Image As"
        )

        if file_path:
            self.image_method.get(0)(file_path)#save image
            self.image_method.get(1)(file_path)#set path



    def hold_mouse_action(self,event):
        if self.mode !=2:#not for drawing shapes
            #offset of the slider
            x_offset = self.h.get()[0] * self.image_w
            y_offset = self.v.get()[0] * self.image_h
            self.prev_position = self.clicked
            self.clicked = [event.x+x_offset, event.y+y_offset]

            # in case the image is larger than the canvas, draw only on the image, not outside of it
            if self.image_w>event.x+x_offset and self.image_h+y_offset>event.y:
                self.methods.get(self.mode)([event.x+x_offset,event.y+y_offset,self.prev_position[0],self.prev_position[1]])#draw



    def left_click_action(self,event):
        x_offset=self.h.get()[0]*self.image_w
        y_offset=self.v.get()[0]*self.image_h
        self.prev_position= [event.x+x_offset, event.y+y_offset]
        self.clicked = [event.x+x_offset, event.y+y_offset]
        if self.mode != 2 and self.image_w>event.x+x_offset and self.image_h>event.y+y_offset:#not for drawing shape
            self.methods.get(self.mode)([event.x+x_offset,event.y+y_offset,self.prev_position[0],self.prev_position[1]])#draw dot


    def release(self,event):
        if (self.mode !=0 and self.mode !=1) and self.image_w>self.clicked[0] and self.image_h>self.clicked[1]:#not for drawing with the brush oe erasing
            x_offset = self.h.get()[0] * self.image_w
            y_offset = self.v.get()[0] * self.image_h
            x0=self.clicked[0]
            x1=event.x+x_offset
            if x1<x0:
                x1=x0
                x0=event.x+x_offset

            y0=self.clicked[1]
            y1=event.y+y_offset
            if y1 < y0:
                y1=y0
                y0 = event.y+y_offset
            self.methods.get(self.mode)([self.shape,[x0,y0,x1,y1]])#draw shape

    def draw_button_click(self):
        self.mode=0
        self.draw_button.config(bg=self.theme.get("button_active"))
        self.erase_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button"))
    def erase_button_click(self):
        self.mode=1
        self.draw_button.config(bg=self.theme.get("button"))
        self.erase_button.config(bg=self.theme.get("button_active"))
        self.shape_button.config(bg=self.theme.get("button"))

    def shape_button_click(self):
        self.shape_menu.post(self.shape_button.winfo_rootx(),
                            self.shape_button.winfo_rooty() + self.shape_button.winfo_height())

    def create_line(self):
        self.mode=2
        self.draw_button.config(bg=self.theme.get("button"))
        self.erase_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button_active"))
        self.shape=0
    def create_rectangle(self):
        self.mode = 2
        self.draw_button.config(bg=self.theme.get("button"))
        self.erase_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button_active"))
        self.shape =1
    def create_circle(self):
        self.mode = 2
        self.draw_button.config(bg=self.theme.get("button"))
        self.erase_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button_active"))
        self.shape=2
        
    def create_perspective(self):
        self.draw_button.config(bg=self.theme.get("button"))
        self.erase_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button_active"))
    def size_button_click(self,event):
        self.slider_frame.place(x=self.size_button_frame_border.winfo_x(),
                               y=self.size_button_frame_border.winfo_y()+self.size_button_frame_border.winfo_height())
        self.size_slider.set(self.brush.get(3)())



    def get_slider_value(self,value):
        self.brush.get(0)(int(value))
        self.size_ind.config(text=value)


    def hide_slider(self):
        self.slider_frame.place_forget()
    def color_button_click(self,event):
        color=colorchooser.askcolor()[1]
        self.brush.get(1)(color)
        self.fg_color_image = Image.new('RGB', (35, 17), color=color)
        self.fg_photo = ImageTk.PhotoImage(self.fg_color_image)
        self.fg_color.config(image=self.fg_photo)

    def fill_button_click(self,event):
        color=colorchooser.askcolor()[1]
        self.brush.get(2)(color)
        self.bg_color_image = Image.new('RGB', (35, 17), color=color)
        self.bg_photo = ImageTk.PhotoImage(self.bg_color_image)
        self.bg_color.config(image=self.bg_photo)

    def remove_fill_click(self):
        self.brush.get(4)()
        self.bg_color_image = Image.new('RGBA', (35, 17), (0,0,0,0))
        self.bg_photo = ImageTk.PhotoImage(self.bg_color_image)
        self.bg_color.config(image=self.bg_photo)

    def select_button_click(self):
        print("hello")

    def transform_button_click(self):
        print("hello")




