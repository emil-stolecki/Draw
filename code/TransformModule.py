class TransformModule:

    def __init__(self):


        self.transforming_image = None  # image


        self.location={
            "active_outline": None, #id
            "offset":()#offset from (0,0) of the canvas
        }

        self.rotation={
            "active_outline" : None,#id,
            "outline_coords":None, #[]
            "center_dot": None,#id
            "offset":(0,0),
            "angle":0,
            "center":(0,0)
        }

        self.scaling={
            "active_outline": None,  # id,
            "handles":[],
            "active_handle":None,
            "offset":(0,0),
            "previous_outline_coords": None

        }