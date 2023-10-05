class Clipboard:
    def __init__(self):

        self.copied_piece = None
        self.transforming_image=None

    def assign_copied(self,copied):
        self.copied_piece=copied

    def get_copied(self):
        return self.copied_piece

    def assign_transforming(self,image):
        self.transforming_image=image

