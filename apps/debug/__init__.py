import sys
import os

sys.path.insert(0, "/system/apps/debug")
os.chdir("/system/apps/debug")

from badgeware import brushes

from scroll_list import ScrollList

# Constants for os.ilistdir() output (Source: https://docs.micropython.org/en/v1.26.0/library/os.html#os.ilistdir)
NAME, TYPE, INODE, SIZE = 0, 1, 2, 3
FILE = 0x8000
DIR = 0x4000


class FileList(ScrollList):
    def __init__(self):
        super().__init__("File System")
        self.current_dir = "/"
        self.cd(self.current_dir)

    def render_item(self, item, index):
        brush = (
            brushes.color(0, 0, 255)
            if item[TYPE] == DIR
            else brushes.color(255, 255, 255)
        )
        return super().render_item(item[NAME], index, brush=brush)

    def on_button_back(self):
        self.cd(parent_of(self.current_dir))

    def on_button_select(self):
        if self.index is not None and self.content_items[self.index][TYPE] == DIR:
            new_dir = joined(self.current_dir, self.content_items[self.index][NAME])
            self.cd(new_dir)

    def cd(self, to_dir):
        self.current_dir = to_dir
        self.subtitle_text = to_dir
        self.content_items = items_of(to_dir)
        self.index = None


def items_of(folder):
    return sorted(os.ilistdir(folder), key=lambda x: x[NAME])


def parent_of(dir):
    return "/".join(dir.split("/")[:-1]) or "/"


def joined(dir1, dir2):
    prefix = dir1 if dir1 == "/" else f"{dir1}/"
    return f"{prefix}{dir2}"


########################################################################################
# App entry points
########################################################################################

filelist = FileList()


def update():
    filelist.update()
