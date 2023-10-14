class Click:
    #This class holds methods that are called after mouse events
    def __init__(self,methods):
        self.prev_position=[]
        self.clicked = []
        self.temp_item_start_position=(0,0)
        self.image_size=(1000,800)
        self.click={
            0:self.click_draw,
            1:self.click_shape,
            2:self.click_select,
            3:self.click_transform
        }
        self.drag = {
            0:self.drag_draw,
            1:self.drag_shape,
            2:self.drag_select,
            3:self.drag_transform
        }
        self.release = {
            0:self.release_draw,
            1:self.release_shape,
            2:self.release_select,
            3:self.release_transform
        }
        self.methods = methods
        # 0-draw
        # 1-create_shape
        # 2-select
        # 3-transform


    def click_draw(self,args):#args: (event.x, event.y, offset_x, offset_y)
        im_w,im_h=self.image_size
        if im_w>args[0] + args[2] and im_h>args[1] + args[3]:
            self.prev_position = [args[0] + args[2], args[1] + args[3]]
            self.methods.get(0)(
                [args[0] + args[2], args[1] + args[3], self.prev_position[0], self.prev_position[1]])  # draw dot

    def click_shape(self,args):#args: (event.x, event.y, offset_x, offset_y,shape)
        self.temp_item_start_position = (args[0] + args[2], args[1] + args[3])
        if args[4] == 0:
            self.preview_item = self.canvas.create_line(args[0] + args[2], args[1] + args[3],args[0] + args[2], args[1] + args[3], width=1)
        if args[4] == 1:
            self.preview_item = self.canvas.create_rectangle(event.x + x_offset, event.y + y_offset, event.x + x_offset,
                                                             event.y + y_offset, width=1)
        if args[4] == 2:
            self.preview_item = self.canvas.create_oval(event.x + x_offset, event.y + y_offset, event.x + x_offset,
                                                        event.y + y_offset, width=1)

    def click_select(self,args):
        pass
    def click_transform(self,args):
        pass



    def drag_draw(self,args):#args: (event.x, event.y, offset_x, offset_y,image_w,image_h)
        self.prev_position = self.clicked
        self.clicked = [args[0] + args[2], args[1] + args[3]]
        im_w, im_h = self.image_size
        if im_w > args[0] + args[2] and im_h > args[1] + args[3]:
            self.methods.get(0)(
                [args[0] + args[2], args[1] + args[3], self.prev_position[0], self.prev_position[1]])  # draw

    def drag_shape(self,args):
        pass

    def drag_select(self,args):
        pass

    def drag_transform(self,args):
        pass



    def release_draw(self,args):
        pass

    def release_shape(self,args):
        pass

    def release_select(self,args):
        pass

    def release_transform(self,args):
        pass
