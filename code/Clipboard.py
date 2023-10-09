class Clipboard:
    def __init__(self):

        self.copied_piece = None
        self.copied_og_coords=[]
        self.backup_image=None


    def assign_copied(self,copied,coords):
        self.copied_piece=copied
        self.copied_og_coords=coords

    def get_copied(self):
        return self.copied_piece

    def get_copied_coords(self):
        return self.copied_og_coords

    def assign_backup(self,image):
        self.backup_image=image



