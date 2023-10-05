from tkinter import *
from PIL import ImageTk,Image,ImageDraw
from tkinter import filedialog,colorchooser
from ImageModel import ImageModel

class Display:
    def __init__(self,methods,image_method,brush_methods,clipboard):
        self.mode=0
        # 0-draw
        # 1-create shape
        # 2-copy
        # 3-cut
        # 4-paste
        # 5-apply

        self.shape=0
        # 0-line
        # 1-rectangle
        # 2-circle
        # 3-perspective
        self.transform_mode=0
        # 0-move
        # 1-rotate
        # 2-scale
        self.methods = methods
        #0-draw
        #1-create_shape
        #2-select
        #3-transform
        self.image_method = image_method
        #0-save_image
        #1-img.set_path
        #2-img.get_path
        #3-new_image
        #4-img.get_image
        self.brush = brush_methods
        #0-brush.change_size
        #1-brush.change_color
        #2-brush.change_fill
        #3-brush.get_size
        #4-brush.remove_fill
        self.clipboard=clipboard
        #0-asign_copied
        #1-get_copied

        self.prev_position=[]
        self.clicked=[]
        self.preview_item = None
        self.selected_area=None
        self.temp_item_start_position = (0,0)
        self.pasted_piece=None
        self.pasted_photo=None

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
        self.file_menu.add_command(label="Save", command=self._save_chosen)
        self.file_menu.add_command(label="Save as...", command=self._save_as_chosen)

        self.draw_button = Button( self.buttons_bar , text="Draw",command=self._draw_button_click,height=2,width=5,bg=self.theme.get("button_active"))
        self.draw_button.pack(side="left")

        # shape_button
        self.shape_button = Button(self.buttons_bar, text="Shape", command=self._shape_button_click, height=2, width=5,
                                   bg=self.theme.get("button"))
        self.shape_button.pack(side="left")
        #shape_button's drop down menu
        self.shape_menu = Menu(self.root, tearoff=0)
        self.shape_menu.add_command(label="Line",command=self._create_line)
        self.shape_menu.add_command(label="Rectangle", command=self._create_rectangle)
        self.shape_menu.add_command(label="Circle", command=self._create_circle)
        self.shape_menu.add_command(label="Perspective",command=self._create_perspective)

        #brush size button
        self.size_button_frame_border=Frame(self.buttons_bar,padx=2,pady=2,bg=self.theme.get("button_border"))
        self.size_button_frame = Frame(self.size_button_frame_border,padx=8,bg=self.theme.get("button"))
        self.size_button_frame.pack()

        size_label = Label(self.size_button_frame, text="Size",bg=self.theme.get("button"))
        size_label.pack()
        self.size_ind = Label(self.size_button_frame, text="6",bg=self.theme.get("button"))
        self.size_ind.pack()

        self.size_button_frame.bind("<Button-1>", self._size_button_click)
        size_label.bind("<Button-1>", self._size_button_click)
        self.size_ind.bind("<Button-1>", self._size_button_click)

        self.size_button_frame_border.pack(side="left")
        #slider
        self.slider_frame=LabelFrame(self.root)
        self.size_slider=Scale(self.slider_frame,orient="horizontal",width=15, from_=1,to=100, command=self._get_slider_value)
        self.size_slider.grid(row=0, column=0)
        self.confirm_size=Button(self.slider_frame, text="X",command=self._hide_slider)
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

        self.fg_color_frame.bind("<Button-1>", self._color_button_click)
        fg_name_label.bind("<Button-1>", self._color_button_click)
        self.fg_color.bind("<Button-1>", self._color_button_click)

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

        self.bg_color_frame.bind("<Button-1>",self._fill_button_click)
        bg_name_label.bind("<Button-1>", self._fill_button_click)
        self.bg_color.bind("<Button-1>", self._fill_button_click)

        self.bg_color_frame_border.pack(side="left")

        #remove fill
        self.remove_fill_button = Button(self.buttons_bar , text="No Fill",command=self._remove_fill_click,height=2,width=5,bg=self.theme.get("button"))
        self.remove_fill_button.pack(side="left")

        #selection
        self.select_button = Button(self.buttons_bar , text="Select",command=self._select_button_click,height=2,width=5,bg=self.theme.get("button"))
        self.select_button.pack(side="left")

        self.selection_menu = Menu(self.root, tearoff=0)
        self.selection_menu.add_command(label="Rectangle", command=self._select_with_rectangle)
        self.selection_menu.add_command(label="Circle", command=self._select_with_elipse)
        self.selection_menu.add_command(label="Free-form", command=self._select_with_free_form)
        self.selection_menu.add_command(label="No Selection", command=self._no_selection)

        #transform
        self.transform_button = Button( self.buttons_bar , text="Transform",command=self._transform_button_click,height=2,width=5,bg=self.theme.get("button"))
        self.transform_button.pack(side="left")

        self.transform_menu = Menu(self.root, tearoff=0)
        self.transform_menu.add_command(label="Move", command=self._move)
        self.transform_menu.add_command(label="Rotate", command=self._rotate)
        self.transform_menu.add_command(label="Scale", command=self._scale)

        #scroll panes for the workspace
        self.h = Scrollbar(self.workspace, orient='horizontal')
        self.h.pack(side=BOTTOM, fill=X)
        self.v = Scrollbar(self.workspace)
        self.v.pack(side=RIGHT, fill=Y)

        #create canvas - only for displaying changes
        self.canvas = Canvas(self.workspace, width=1000,height=800,xscrollcommand=self.h.set, yscrollcommand=self.v.set)
        self.canvas.pack(fill="both", expand=True)
        self.h.config(command=self.canvas.xview)
        self.v.config(command=self.canvas.yview)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        # mouse events
        self.canvas.bind("<Button-1>", self._left_click_action)
        self.canvas.bind("<B1-Motion>", self._hold_mouse_action)
        self.canvas.bind("<ButtonRelease-1>",self._release)
        self.canvas.bind("<Button-3>",self._right_click)


        #image for the canvas
        self.image_w=1000
        self.image_h=800
        image = Image.new('RGB', (1000, 800), (255, 255, 255))
        self.photo_image=ImageTk.PhotoImage(image)
        self.background_image=self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)

        # placeholder for layers
        self.myLabel3 = Label(self.layers, text="Layers", padx=100)
        self.myLabel3.pack()

        #copy_mode menu
        self.copy_mode_menu = Menu(self.root, tearoff=0)
        self.copy_mode_menu.add_command(label="copy", command=self._copy)
        self.copy_mode_menu.add_command(label="cut", command=self._cut)
        self.copy_mode_menu.add_command(label="paste", command=self._paste)

        #transform_mode menu
        self.transform_mode_menu=Menu(self.root, tearoff=0)
        self.transform_mode_menu.add_command(label="apply",command=self._apply_transform)
        self.transform_mode_menu.add_command(label="cancel", command=self._cancel_transform)

    def loop(self):

        self.root.mainloop()

    def file_button_click(self):

        self.file_menu.post(self.file_button.winfo_rootx(), self.file_button.winfo_rooty() + self.file_button.winfo_height())

    #creates new canvas
    def new_chosen(self):
        #create new image
        image = Image.new('RGB', (1000,800), (255, 255, 255))
        self.image_method.get(3)(image)#attach new image
        #create  new display
        self.canvas.destroy()
        self.canvas = Canvas(self.workspace, width=1000,height=800,xscrollcommand=self.h.set, yscrollcommand=self.v.set)
        self.photo_image = ImageTk.PhotoImage(image)
        self.background_image=self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
        self.h.config(command=self.canvas.xview)
        self.v.config(command=self.canvas.yview)
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._left_click_action)
        self.canvas.bind("<B1-Motion>", self._hold_mouse_action)
        self.canvas.bind("<ButtonRelease-1>", self._release)
        self.canvas.bind("<Button-3>", self._right_click)


   #OPEN/SAVE
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
            self.background_image=self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
            self.h.config(command=self.canvas.xview)
            self.v.config(command=self.canvas.yview)
            self.canvas.config(scrollregion=self.canvas.bbox(ALL))
            self.canvas.pack(fill="both", expand=True)
            self.canvas.bind("<Button-1>", self._left_click_action)
            self.canvas.bind("<B1-Motion>", self._hold_mouse_action)
            self.canvas.bind("<ButtonRelease-1>", self._release)
            self.canvas.bind("<Button-3>", self._right_click)

    def _save_chosen(self):
        if self.image_method.get(2)():#check if path exists
            self.image_method.get(0)(self.image_method.get(2)())#save
        else:
            self._save_as_chosen()
    def _save_as_chosen(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")),
            title="Save Image As"
        )

        if file_path:
            self.image_method.get(0)(file_path)#save image
            self.image_method.get(1)(file_path)#set path


    #MOUSE EVENTS

    def _left_click_action(self,event):
        x_offset=self.h.get()[0]*self.image_w
        y_offset=self.v.get()[0]*self.image_h
        self.clicked = [event.x + x_offset, event.y + y_offset]
        # for drawing
        if self.mode ==0 and self.image_w>event.x+x_offset and self.image_h>event.y+y_offset:
            self.prev_position = [event.x + x_offset, event.y + y_offset]
            self.methods.get(self.mode)([event.x+x_offset,event.y+y_offset,self.prev_position[0],self.prev_position[1]])#draw dot
        #for creating shapes
        if self.mode ==1:#create an item on canvas that will be used as preview
            self.temp_item_start_position=(event.x+x_offset,event.y+y_offset)
            if self.shape==0:
                self.preview_item=self.canvas.create_line(event.x+x_offset,event.y+y_offset,event.x+x_offset,event.y+y_offset,width=1)
            if self.shape==1:
                self.preview_item=self.canvas.create_rectangle(event.x+x_offset,event.y+y_offset,event.x+x_offset,event.y+y_offset,width=1)
            if self.shape==2:
                self.preview_item=self.canvas.create_oval(event.x+x_offset,event.y+y_offset,event.x+x_offset,event.y+y_offset,width=1)
        #for selecting
        if self.mode ==2:#create an item on canvas that will be used as preview
            if self.selected_area:  # delete old if exists
                self.canvas.delete(self.selected_area)
            self.temp_item_start_position = (event.x + x_offset, event.y + y_offset)
            if self.shape==1:#select with rectangle
                self.selected_area=self.canvas.create_rectangle(event.x+x_offset,event.y+y_offset,event.x+x_offset,event.y+y_offset,width=1,dash=(2,2))
            if self.shape==2:#select with elipse
                pass
                self.selected_area=self.canvas.create_oval(event.x+x_offset,event.y+y_offset,event.x+x_offset,event.y+y_offset,width=1,dash=(2,2))
        #for transforming
        if self.mode == 3:
            self.prev_position = [event.x + x_offset, event.y + y_offset]
            if self.pasted_piece==None: #if there is no image to transform, make one from selection

                if self.selected_area: #transform selection
                    self._cut()
                    self._paste()

                else: # if there is no active selection select whole image/layer
                    self._flatten_image()
                    og_img = self.image_method.get(4)()
                    self.clipboard.get(0)(og_img)
                    new_image = Image.new("RGBA", size=og_img.size,color=(0,0,0,0))
                    self.clipboard.get(2)(new_image)
                    self.selected_area = self.canvas.bbox(self.background_image)
                    self.temp_item_start_position = (0, 0)
                    self.pasted_piece=self.background_image

    def _hold_mouse_action(self,event):
        # offset of the slider
        x_offset = self.h.get()[0] * self.image_w
        y_offset = self.v.get()[0] * self.image_h
        if self.mode ==0:#drawing
            self.prev_position = self.clicked
            self.clicked = [event.x+x_offset, event.y+y_offset]

            # in case the image is larger than the canvas, draw only on the image, not outside of it
            if self.image_w>event.x+x_offset and self.image_h+y_offset>event.y:
                self.methods.get(self.mode)([event.x+x_offset,event.y+y_offset,self.prev_position[0],self.prev_position[1]])#draw

        if self.mode ==1:#creating shapes (preview)
            self.canvas.delete(self.preview_item)#delete old create new
            x0,y0=self.temp_item_start_position
            x1,y1=event.x + x_offset, event.y + y_offset
            if self.shape!=0:
                if x1<x0:
                    x1=x0
                    x0=event.x+x_offset
                if y1 < y0:
                    y1=y0
                    y0 = event.y+y_offset
            if self.shape == 0:
                self.preview_item = self.canvas.create_line(x0,y0,x1,y1, width=1)
            if self.shape == 1:
                self.preview_item = self.canvas.create_rectangle(x0,y0,x1,y1, width=1)
            if self.shape == 2:
                self.preview_item = self.canvas.create_oval(x0,y0,x1,y1, width=1)

        if self.mode ==2:#selection (preview)
            self.canvas.delete(self.selected_area)#delete old create new
            x0,y0=self.temp_item_start_position
            x1,y1=event.x + x_offset, event.y + y_offset
            if self.shape!=0:
                if x1<x0:
                    x1=x0
                    x0=event.x+x_offset
                if y1 < y0:
                    y1=y0
                    y0 = event.y+y_offset
            if self.shape == 0:
                self.selected_area = self.canvas.create_line(x0,y0,x1,y1, width=1,dash=(2,2))
            if self.shape == 1:
                self.selected_area = self.canvas.create_rectangle(x0,y0,x1,y1, width=1,dash=(2,2))
            if self.shape == 2:
                self.selected_area = self.canvas.create_oval(x0,y0,x1,y1, width=1,dash=(2,2))
        # for transforming
        if self.mode == 3:
            if self.transform_mode==0:#move
                x0, y0 = self.temp_item_start_position
                x=event.x-self.prev_position[0]+x0
                y=event.y-self.prev_position[1]+y0
                self.canvas.moveto(self.pasted_piece,x,y)
            if self.transform_mode==1:#rotare
                pass
            if self.transform_mode==2:#scale
                pass


    def _release(self,event):
        # for creating shapes
        if self.mode ==1 and self.image_w>self.clicked[0] and self.image_h>self.clicked[1]:
            x_offset = self.h.get()[0] * self.image_w
            y_offset = self.v.get()[0] * self.image_h
            x0=self.clicked[0]
            x1=event.x+x_offset
            y0 = self.clicked[1]
            y1 = event.y + y_offset
            if self.shape!=0:
                if x1<x0:
                    x1=x0
                    x0=event.x+x_offset
                if y1 < y0:
                    y1=y0
                    y0 = event.y+y_offset
            self.canvas.delete(self.preview_item)
            self.methods.get(self.mode)([self.shape,[x0,y0,x1,y1]])#draw shape
            self.temp_item_start_position=(0,0)#reset
        # for selection
        if self.mode == 2:
            self.canvas.itemconfigure(self.selected_area, outline="red")
            self.temp_item_start_position=(0,0)#reset
        #for transform
        if self.mode ==3:
            self.temp_item_start_position=self.canvas.coords(self.pasted_piece)


    def _right_click(self,event):
        x_offset=self.root.winfo_x()+self.frame.winfo_x()+self.canvas.winfo_x()+12
        y_offset=self.root.winfo_y()+self.frame.winfo_y()+self.canvas.winfo_y()+35
        if self.mode==2:
            self.copy_mode_menu.post(event.x+x_offset,event.y+y_offset)
        if self.mode==3:
            self.transform_mode_menu.post(event.x+x_offset,event.y+y_offset)
   #DRAWING/CREATING SHAPES BUTTONS
    def _draw_button_click(self):
        self.mode=0
        self.draw_button.config(bg=self.theme.get("button_active"))
        self.shape_button.config(bg=self.theme.get("button"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button"))
        self._cancel_transform()


    def _shape_button_click(self):
        self.shape_menu.post(self.shape_button.winfo_rootx(),
                            self.shape_button.winfo_rooty() + self.shape_button.winfo_height())

    def _create_line(self):
        self.mode=1
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button_active"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button"))
        self.shape=0

    def _create_rectangle(self):
        self.mode = 1
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button_active"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button"))
        self.shape =1
    def _create_circle(self):
        self.mode = 1
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button_active"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button"))
        self.shape=2
        
    def _create_perspective(self):
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button_active"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button"))


    #MODIFY THE BRUSH
    def _size_button_click(self,event):
        self.slider_frame.place(x=self.size_button_frame_border.winfo_x(),
                               y=self.size_button_frame_border.winfo_y()+self.size_button_frame_border.winfo_height())
        self.size_slider.set(self.brush.get(3)())



    def _get_slider_value(self,value):
        self.brush.get(0)(int(value))
        self.size_ind.config(text=value)


    def _hide_slider(self):
        self.slider_frame.place_forget()
    def _color_button_click(self,event):
        color=colorchooser.askcolor()[1]
        self.brush.get(1)(color)
        self.fg_color_image = Image.new('RGB', (35, 17), color=color)
        self.fg_photo = ImageTk.PhotoImage(self.fg_color_image)
        self.fg_color.config(image=self.fg_photo)

    def _fill_button_click(self,event):
        color=colorchooser.askcolor()[1]
        self.brush.get(2)(color)
        self.bg_color_image = Image.new('RGB', (35, 17), color=color)
        self.bg_photo = ImageTk.PhotoImage(self.bg_color_image)
        self.bg_color.config(image=self.bg_photo)

    def _remove_fill_click(self):
        self.brush.get(4)()
        self.bg_color_image = Image.new('RGBA', (35, 17), (0,0,0,0))
        self.bg_photo = ImageTk.PhotoImage(self.bg_color_image)
        self.bg_color.config(image=self.bg_photo)


    #
    def _flatten_image(self):
        img=self.image_method.get(4)()
        self.photo_image = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.background_image=self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
        self.selected_area=None
        self.pasted_piece=None




    def _select_button_click(self):
        self.selection_menu.post(self.select_button.winfo_rootx(),
                             self.select_button.winfo_rooty() + self.select_button.winfo_height())

        self._flatten_image()

    def _select_with_rectangle(self):
        self.mode=2
        self.shape=1
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button"))
        self.select_button.config(bg=self.theme.get("button_active"))
        self.transform_button.config(bg=self.theme.get("button"))
        self._cancel_transform()
    def _select_with_elipse(self):
        self.mode = 2
        self.shape = 2
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button"))
        self.select_button.config(bg=self.theme.get("button_active"))
        self.transform_button.config(bg=self.theme.get("button"))
        self._cancel_transform()
    def _select_with_free_form(self):
        self.mode = 2
        self.shape = 3
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button"))
        self.select_button.config(bg=self.theme.get("button_active"))
        self.transform_button.config(bg=self.theme.get("button"))
        self._cancel_transform()


    def _no_selection(self):
        self.canvas.delete(self.selected_area)
        self.selected_area=None

    def _copy(self):
        if self.selected_area:
            bbox = self.canvas.coords(self.selected_area)
            self.methods.get(2)(bbox,self.shape)

            
    def _cut(self):
        bbox = self.canvas.coords(self.selected_area)
        new_image=self.methods.get(3)(bbox,self.shape)
        #update canvas
        self.photo_image = ImageTk.PhotoImage(new_image)
        self.canvas.delete("all")
        self.background_image = self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
    def _paste(self):
        piece=self.clipboard.get(1)()
        if piece:
            self.pasted_photo=ImageTk.PhotoImage(piece)
            self.pasted_piece =self.canvas.create_image(0, 0, anchor=NW, image=self.pasted_photo)

    def _transform_button_click(self):
        self.transform_menu.post(self.transform_button.winfo_rootx(),
                                 self.transform_button.winfo_rooty() + self.transform_button.winfo_height())

    def _move(self):
        self.mode = 3
        self.transform_mode=0
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button_active"))

    def _rotate(self):
        self.mode = 3
        self.transform_mode=1
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button_active"))


    def _scale(self):
        self.mode = 3
        self.transform_mode=2
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button_active"))



    def _apply_transform(self):
        x,y=self.temp_item_start_position
        self.methods.get(5)(x,y)
        self._flatten_image()

    def _cancel_transform(self):
        self.clipboard.get(2)(None)
        self._flatten_image()


