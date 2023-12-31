import math
from tkinter import *
from PIL import ImageTk,Image,ImageDraw
from tkinter import filedialog,colorchooser

from PIL.Image import Resampling

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
        #2-asign transforming image

        self.prev_position=[]
        self.clicked=[]

        self.preview_item=None#id
        self.selected_area=None#id
        self.pasted_piece = None  # id
        self.active_transformation_outline = None  # id
        self.active_rotation_outline = None  # id
        self.rotation_center_dot = None  # id
        self.active_scaling_outline=None#id
        self.scaling_handles=[]
        self.active_scaling_handle=None
        self.temp_item_start_position = (0,0)#pasted layer's top left corner
        self.rotation_outline_coords=None #[]
        self.rotated_piece_offset=(0,0)
        self.scaled_piece_offset=(0,0)
        self.angle=0
        self.rotation_center=(0,0)
        self.clicks_since_handle = -1
        self.previous_scaling_outline_coords=None
        self.pasted_photo = None
        self.transforming_image=None#image


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
        self.slider_frame=Frame(self.root)
        self.size_slider=Scale(self.slider_frame,orient="horizontal",width=15,length=100, from_=1,to=100, command=self._get_size_slider_value)
        self.size_slider.grid(row=0, column=0)
        self.confirm_size=Button(self.slider_frame, text="X",command=self._hide_size_slider)
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

        self.rotation_menu=Frame(self.root,bd=3)
        rot_menu_label=Label(self.rotation_menu,text='<-left ROTATE right->')
        rot_menu_label.grid(row=0,column=2)
        self.angle_slider = Scale(self.rotation_menu, orient="horizontal", width=15, length=360,from_=-180, to=180,
                                  command=self._get_angle_slider_value)

        self.angle_slider.grid(row=1, column=0,columnspan=5)
        self.confirm_angle = Button(self.rotation_menu, text="X", command=self._hide_angle_slider)
        self.confirm_angle.grid(row=0, column=5)
        rotation_apply_button=Button(self.rotation_menu,text="Apply",command=self._apply_rotation)
        rotation_reset_button=Button(self.rotation_menu,text="Reset",command=self._reset_rotation)

        rotation_apply_button.grid(row=2,column=1)
        rotation_reset_button.grid(row=2,column=3)








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
        #reset
        self.temp_item_start_position = (0, 0)
        self.rotation_outline_coords = None
        self.rotated_piece_offset = (0, 0)
        self.rotation_center = (0, 0)
        self.scaled_piece_offset = (0, 0)
        self.preview_item = None  # id
        self.selected_area = None  # id
        self.pasted_piece = None  # id
        self.active_transformation_outline = None  # id
        self.active_rotation_outline = None  # id
        self.rotation_center_dot = None
        self.active_scaling_outline = None  # id
        self.scaling_handles = []



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
            # reset
            self.temp_item_start_position = (0, 0)
            self.rotation_outline_coords = None
            self.rotated_piece_offset = (0, 0)
            self.rotation_center = (0, 0)
            self.scaled_piece_offset = (0, 0)
            self.preview_item = None  # id
            self.selected_area = None  # id
            self.pasted_piece = None  # id
            self.active_transformation_outline = None  # id
            self.active_rotation_outline = None  # id
            self.rotation_center_dot = None
            self.active_scaling_outline = None  # id
            self.scaling_handles = []

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
                self.selected_area=self.canvas.create_rectangle(event.x+x_offset,event.y+y_offset,event.x+x_offset,event.y+y_offset,width=1,dash=(2,2),tags='selection')
            if self.shape==2:#select with elipse
                pass
                self.selected_area=self.canvas.create_oval(event.x+x_offset,event.y+y_offset,event.x+x_offset,event.y+y_offset,width=1,dash=(2,2),tags='selection')
        #for transforming
        if self.mode == 3:
            self.prev_position = [event.x + x_offset, event.y + y_offset]
            if self.pasted_piece==None: #if there is no image to transform, make one from selection

                if self.selected_area: #transform selection
                    self._cut(False)#save the original image in case the tranformation gets cancelled or interrupted
                    self._paste()

                else: # if there is no active selection select whole image/layer
                    self._flatten_image()
                    og_img = self.image_method.get(4)()##get whole image
                    self.transforming_image = og_img
                    bbox= self.canvas.bbox(self.background_image)
                    self.clipboard.get(0)(og_img,bbox)#save the image and bbox to clipboard
                    new_image = Image.new("RGBA", size=og_img.size,color=(0,0,0,0))#new background
                    self.clipboard.get(2)(new_image)#save as backup
                    self.selected_area = self.canvas.create_rectangle(bbox, width=1,dash=(2,2),outline="red", tags='selection')
                    self.active_transformation_outline = self.canvas.create_rectangle(bbox, width=1,dash=(2,2),outline="blue", tags='selection')
                    self.temp_item_start_position = (0, 0)
                    self.pasted_piece=self.background_image


            if self.transform_mode==1:#rotation
                if self.rotation_menu.winfo_ismapped()==0:
                    self.rotation_menu.place(x=event.x,y=event.y)
                    self.angle_slider.set("0")
                self.rotation_center=(event.x,event.y)

                if self.active_rotation_outline==None:
                    bbox=[]
                    if self.selected_area:
                        bbox=self.canvas.coords(self.selected_area)
                    else:
                        bbox=self.canvas.bbox(self.background_image)

                    self.active_rotation_outline=self.canvas.create_polygon([(bbox[0],bbox[1]),(bbox[2],bbox[1]),(bbox[2],bbox[3]),(bbox[0],bbox[3])],dash=(2,2),width=1,outline="green",fill="")


                self.canvas.delete(self.rotation_center_dot)
                self.rotation_center_dot=self.canvas.create_oval(event.x-2,event.y-2,event.x+2,event.y+2,outline="green",fill="red",tags='selection')

            if self.transform_mode == 2:#scale
                self.scaled_image=self.transforming_image
                if self.active_scaling_outline== None:
                    coords=self.canvas.coords(self.active_transformation_outline)
                    self.previous_scaling_outline_coords=coords
                    self.active_scaling_outline=self.canvas.create_rectangle(coords,outline="orange", width=1, dash=(2,2),tags=('selection','scale'))
                    s=4
                    a=self.canvas.create_rectangle(coords[0]-s,coords[1]-s,
                                               coords[0]+s,coords[1]+s,
                                               outline="orange", fill="yellow", width=1 ,tags=('selection','scale'))
                    b = self.canvas.create_rectangle(coords[2] - s, coords[1] - s,
                                                 coords[2] + s, coords[1] + s,
                                                 outline="orange", fill="yellow", width=1, tags=('selection','scale'))
                    c = self.canvas.create_rectangle(coords[2] - s, coords[3] - s,
                                                 coords[2] + s, coords[3] + s,
                                                 outline="orange", fill="yellow", width=1, tags=('selection','scale'))
                    d = self.canvas.create_rectangle(coords[0] - s, coords[3] -s,
                                                 coords[0] + s, coords[3] + s,
                                                 outline="orange", fill="yellow", width=1, tags=('selection','scale'))

                    self.scaling_handles={
                        "a":a,
                        "b":b,
                        "c":c,
                        "d":d
                    }

                    self.canvas.tag_bind(a, '<ButtonPress-1>',self._handle_scaling_a)
                    self.canvas.tag_bind(b, '<ButtonPress-1>', self._handle_scaling_b)
                    self.canvas.tag_bind(c, '<ButtonPress-1>', self._handle_scaling_c)
                    self.canvas.tag_bind(d, '<ButtonPress-1>', self._handle_scaling_d)

                    self.canvas.tag_bind(a, '<ButtonRelease-1>', self._release_handle)
                    self.canvas.tag_bind(b, '<ButtonRelease-1>', self._release_handle)
                    self.canvas.tag_bind(c, '<ButtonRelease-1>', self._release_handle)
                    self.canvas.tag_bind(d, '<ButtonRelease-1>', self._release_handle)


                else:
                    self.canvas.tag_raise('scale')
                    self.previous_scaling_outline_coords = self.canvas.coords(self.active_scaling_outline)
        if self.clicks_since_handle==0 or self.clicks_since_handle==1:
            self.clicks_since_handle=self.clicks_since_handle+1


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
            if self.shape == 1:
                self.selected_area = self.canvas.create_rectangle(x0,y0,x1,y1, width=1,dash=(2,2),tags='selection')
            if self.shape == 2:
                self.selected_area=ted_area = self.canvas.create_oval(x0,y0,x1,y1, width=1,dash=(2,2),tags='selection')
            if self.shape==3:
                pass
        # for transforming
        if self.mode == 3:
            if self.transform_mode==0:#move
                x0, y0 = self.temp_item_start_position
                x=event.x-self.prev_position[0]+x0
                y=event.y-self.prev_position[1]+y0
                og=[0,0]
                s_x, s_y = self.scaled_piece_offset
                og=self.clipboard.get(3)()

                self.canvas.moveto(self.pasted_piece,x,y)

                if self.active_rotation_outline:
                    r_x, r_y = self.rotated_piece_offset


                    self.canvas.moveto(self.active_transformation_outline, x + og[0]+r_x+s_x, y + og[1]+r_y+s_y)
                    self.canvas.moveto(self.active_rotation_outline, x + og[0]+r_x+s_x, y + og[1]+r_y+s_y)
                    self.rotation_outline_coords=self.canvas.coords(self.active_rotation_outline)

                else:
                    if self.active_transformation_outline:
                        self.canvas.moveto(self.active_transformation_outline, x + og[0]+s_x, y + og[1]+s_y)


            if self.transform_mode==2:#scale
                if self.clicks_since_handle==1 :

                    handles=list(self.scaling_handles.values())
                    #0 upper left
                    #1 upper right
                    #2-lower right
                    #3 lower left

                    h=handles.index(self.active_scaling_handle)

                    self.canvas.moveto(self.active_scaling_handle,event.x+4,event.y+4)

                    if h==0:#1.y,3.x
                        self.canvas.moveto(self.scaling_handles.get("b"), y=event.y+4)
                        self.canvas.moveto(self.scaling_handles.get("d"), x=event.x+4)
                    if h==1:#0.y,2.x
                        self.canvas.moveto(self.scaling_handles.get("a"), y=event.y + 4)
                        self.canvas.moveto(self.scaling_handles.get("c"), x=event.x + 4)
                    if h==2:#1.x,3.y
                        self.canvas.moveto(self.scaling_handles.get("b"), x=event.x + 4)
                        self.canvas.moveto(self.scaling_handles.get("d"), y=event.y + 4)
                    if h==3:#2.y,0.x
                        self.canvas.moveto(self.scaling_handles.get("c"), y=event.y + 4)
                        self.canvas.moveto(self.scaling_handles.get("a"), x=event.x + 4)
                    a=self.canvas.coords(self.scaling_handles.get("a"))
                    c= self.canvas.coords(self.scaling_handles.get("c"))
                    self.canvas.delete(self.active_scaling_outline)
                    self.active_scaling_outline = self.active_scaling_outline = self.canvas.create_rectangle(a[0]+4,a[1]+4,c[0]+4,c[1]+4,
                                                                                                             outline="orange",width=1,
                                                                                                             dash=(2, 2),tags=('selection','scale'))

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


        if self.selected_area:
            self.canvas.tag_raise(self.selected_area)




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

    def _get_size_slider_value(self,value):
        self.brush.get(0)(int(value))
        self.size_ind.config(text=value)

    def _hide_size_slider(self):
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
        self.canvas.delete('!selection')
        self.background_image=self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
        self.canvas.tag_raise('selection')
        self.pasted_piece=None
        self.pasted_photo=None
        #self.rotated_piece_offset = (0, 0)





    def _select_button_click(self):
        self.selection_menu.post(self.select_button.winfo_rootx(),
                             self.select_button.winfo_rooty() + self.select_button.winfo_height())

        #self._flatten_image()

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
        self._cancel_transform()#temporary solution, else errors when transforming while no selection
        self.selected_area=None

    def _copy(self):
        if self.selected_area:
            bbox = self.canvas.coords(self.selected_area)
            self.methods.get(2)(bbox,self.shape)


    def _cut(self,ispermanent=True):
        bbox = self.canvas.coords(self.selected_area)
        new_image=self.methods.get(3)(bbox,self.shape,ispermanent)
        #save active selection
        if self.selected_area:
            sel=self.canvas.coords(self.selected_area)
        #update canvas
        self.photo_image = ImageTk.PhotoImage(new_image)
        self.canvas.delete('!selection')
        self.background_image = self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)


    def _paste(self):
        piece=self.clipboard.get(1)()
        if piece:
            self.transforming_image = piece
            self.pasted_photo=ImageTk.PhotoImage(piece)
            self.pasted_piece =self.canvas.create_image(0, 0, anchor=NW, image=self.pasted_photo)

            sel=self.clipboard.get(3)()
            if self.shape==1:
                self.active_transformation_outline=self.canvas.create_rectangle(sel,width=1,dash=(2,2),outline="blue",tags='selection')
            if self.shape == 2:
                self.active_transformation_outline = self.canvas.create_oval(sel,width=1, dash=(2, 2),outline="blue",tags='selection')
            if self.shape ==3:
                pass

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
        self.canvas.delete('scale')
        self.active_scaling_outline = None
        self.scaling_handles = None


    def _rotate(self):
        self.mode = 3
        self.transform_mode=1
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button_active"))
        self.canvas.delete('scale')
        self.active_scaling_outline = None
        self.scaling_handles = None






    def _get_angle_slider_value(self,value):
        self.angle=int(value)
        bbox=[]
        if self.rotation_outline_coords:
            c=self.rotation_outline_coords

        else:
            bbox = self.canvas.coords(self.active_transformation_outline)
            c = [bbox[0], bbox[1], bbox[2], bbox[1], bbox[2], bbox[3], bbox[0], bbox[3]]
        coords=[]
        for i in range(0,len(c),2):
            #rotate the preview
            x=c[i]
            y=c[i+1]*-1
            cx,cy=self.rotation_center
            cy=cy*-1

            d = math.sqrt((x - cx) ** 2 + (y -cy ) ** 2)

            angx=math.degrees(math.asin((x-cx)/d))
            angy=math.degrees(math.asin((y-cy)/d))

            angx2 = 0
            angy2 = 0
            if (x - cx)<0 and (y -cy )>0:

                angx2 = (angx + int(value))
                angy2 = (-angy - int(value))

            if (x - cx)<0 and (y -cy )<0:#######
                angx2 = (angx - int(value))
                angy2 = (angy + int(value))

            if (x - cx) > 0 and (y -cy ) > 0:#######
                angx2 = (angx + int(value))
                angy2 =(angy - int(value))

            if (x - cx) > 0 and (y -cy ) < 0:
                angx2 = (angx - int(value))
                angy2 = (-angy + int(value))


            dy = math.sin(math.radians(angy2)) * d
            dx = math.sin(math.radians(angx2)) * d


            if ((x - cx) > 0 and (y -cy ) < 0) or ((x - cx)<0 and (y -cy )>0):
                x = (dx + cx)
                y = (dy - cy)
            else:
                x = dx + cx
                y = -dy - cy

            coords.append((x, y))
        self.canvas.delete(self.active_rotation_outline)
        self.active_rotation_outline = self.canvas.create_polygon(coords, dash=(2, 2), width=1, outline="green", fill="")


        



    def _hide_angle_slider(self):
        self.rotation_menu.place_forget()
        self.canvas.delete(self.rotation_center_dot)
        self.canvas.delete(self.active_rotation_outline)

    def _scale(self):
        self.mode = 3
        self.transform_mode=2
        self.draw_button.config(bg=self.theme.get("button"))
        self.shape_button.config(bg=self.theme.get("button"))
        self.select_button.config(bg=self.theme.get("button"))
        self.transform_button.config(bg=self.theme.get("button_active"))




    def _apply_transform(self):
        if self.active_transformation_outline:
            x,y=self.temp_item_start_position
            self.methods.get(5)(x,y)
            self.canvas.delete(self.active_transformation_outline)
            self.canvas.delete('scale')
            self.active_transformation_outline = None
            self.active_scaling_outline=None
            self.scaling_handles=()
            self.temp_item_start_position=(0,0)
            self._flatten_image()
            self.rotation_menu.place_forget()
            self.transforming_image = None
            self.rotation_outline_coords=None
            self.canvas.delete(self.active_rotation_outline)
            self.active_rotation_outline=None
            self.rotated_piece_offset=(0,0)
            self.scaled_piece_offset =(0,0)







    def _cancel_transform(self):
        self.clipboard.get(2)(None)
        self.canvas.delete(self.active_transformation_outline)
        self.canvas.delete('scale')
        self.active_transformation_outline = None
        self.active_scaling_outline = None
        self.scaling_handles = ()
        self.temp_item_start_position = (0,0)
        self._flatten_image()
        self.rotation_menu.place_forget()
        self.transforming_image=None
        self.rotated_piece_offset = (0,0)
        self.canvas.delete(self.active_rotation_outline)
        self.active_rotation_outline = None
        self.rotation_outline_coords = None
        self.scaled_piece_offset =(0,0)



    def _apply_rotation(self):
        x_offset,y_offset=self.temp_item_start_position

        x,y=self.rotation_center
        img=self.transforming_image

        img = img.rotate(angle=self.angle*-1,center=(x-x_offset,y-y_offset), resample=Resampling.BICUBIC)
        self.transforming_image=img
        self.pasted_photo = ImageTk.PhotoImage(img)
        self.canvas.itemconfigure(self.pasted_piece, image=self.pasted_photo)
        self.rotation_menu.place_forget()
        self.canvas.delete(self.rotation_center_dot)
        self.rotation_outline_coords=self.canvas.coords(self.active_rotation_outline)

        #self.canvas.delete(self.active_rotation_outline)

        x_vals=[]
        y_vals=[]
        for i in range(0,len(self.rotation_outline_coords)-1,2):
            x_vals.append(self.rotation_outline_coords[i])
            y_vals.append(self.rotation_outline_coords[i+1])
        x_max=max(x_vals)
        x_min=min(x_vals)
        y_max = max(y_vals)
        y_min = min(y_vals)

        x_offset=self.canvas.coords(self.active_transformation_outline)[0]
        y_offset=self.canvas.coords(self.active_transformation_outline)[1]
        x_offset = x_min-x_offset
        y_offset = y_min-y_offset


        x1,y1=self.rotated_piece_offset
        self.rotated_piece_offset = (x1+x_offset,y1+y_offset)

        #self.temp_item_start_position=[x_offset, y_offset]
        self.canvas.delete(self.active_transformation_outline)
        self.active_transformation_outline= self.canvas.create_rectangle(x_min,y_min,x_max,y_max,width=1, dash=(2, 2),outline="blue",tags='selection')
        #self.canvas.move(self.active_transformation_outline, x_offset,y_offset)



    def _reset_rotation(self):
        self.transforming_image=self.clipboard.get(1)()
        self.pasted_photo = ImageTk.PhotoImage(self.transforming_image)
        self.canvas.itemconfigure(self.pasted_piece, image=self.pasted_photo)
        #self.rotation_outline_coords=None
        self.canvas.delete(self.active_rotation_outline)
        #self.rotated_piece_offset = (0, 0)

    def _handle_scaling_a(self,event):
        self.active_scaling_handle=self.scaling_handles.get("a")
        self.clicks_since_handle=0

    def _handle_scaling_b(self, event):
        self.active_scaling_handle=self.scaling_handles.get("b")
        self.clicks_since_handle = 0
    def _handle_scaling_c(self, event):
        self.active_scaling_handle=self.scaling_handles.get("c")
        self.clicks_since_handle = 0

    def _handle_scaling_d(self, event):
        self.active_scaling_handle=self.scaling_handles.get("d")
        self.clicks_since_handle = 0

    def _release_handle(self,event):
        img=self.transforming_image


        pre_scaled_coords=self.previous_scaling_outline_coords

        offset=self.canvas.coords(self.pasted_piece)


        coords=(
            pre_scaled_coords[0]-offset[0],
            pre_scaled_coords[1]-offset[1],
            pre_scaled_coords[2]-offset[0],
            pre_scaled_coords[3]-offset[1]
        )

        img=img.crop(coords)
        scaled_coords=self.canvas.coords(self.active_scaling_outline)
        width=int(scaled_coords[2]-scaled_coords[0])
        heigth=int(scaled_coords[3]-scaled_coords[1])
        img=img.resize((width,heigth),Image.Resampling.BICUBIC)

        new_image=Image.new("RGBA", size=self.transforming_image.size)
        new_image.paste(img,(int(scaled_coords[0]-offset[0]),int(scaled_coords[1]-offset[1])),img)

        self.pasted_photo=ImageTk.PhotoImage(new_image)
        self.canvas.itemconfigure(self.pasted_piece, image=self.pasted_photo)
        self.transforming_image=new_image

        self.canvas.delete(self.active_transformation_outline)
        self.active_transformation_outline=self.active_transformation_outline = self.canvas.create_rectangle(scaled_coords, width=1,dash=(2,2),outline="blue", tags='selection')
        #handle 0 (upper left) is the reference for drawing the outline
        #if it's moved, it's necesary to calculate this offset
        sc=self.scaled_piece_offset
        self.scaled_piece_offset=(sc[0]+(scaled_coords[0]-pre_scaled_coords[0]),sc[1]+(scaled_coords[1]-pre_scaled_coords[1]))

