import sys
import os

sys.path.insert(0, "/system/apps/debug")
os.chdir("/system/apps/debug")

from badgeware import PixelFont, screen, brushes, shapes, io, run

small_font = PixelFont.load("/system/assets/fonts/ark.ppf")
large_font = PixelFont.load("/system/assets/fonts/absolute.ppf")

# Constants for os.ilistdir() output (Source: https://docs.micropython.org/en/v1.26.0/library/os.html#os.ilistdir)
NAME, TYPE, INODE, SIZE = 0, 1, 2, 3
FILE = 0x8000
DIR = 0x4000

# Global state
current_dir = "/"
index = None
contents = []


def update():
    global current_dir, index, contents

    if not contents:
        contents = contents_of(current_dir)

    if io.BUTTON_UP in io.pressed:
        index = len(contents) if index == None else (index - 1) % len(contents)

    if io.BUTTON_DOWN in io.pressed:
        index = 0 if index == None else (index + 1) % len(contents)

    if io.BUTTON_B in io.pressed:
        if index is not None and contents[index][TYPE] == DIR:
            new_dir = joined(current_dir, contents[index][NAME])
            cd(new_dir)

    if io.BUTTON_A in io.pressed:
        cd(parent_of(current_dir))

    Draw.background()
    Draw.title()
    Draw.breadcrumb(current_dir)
    Draw.contents(contents, index)


def cd(to_dir):
    global contents, current_dir, index
    current_dir = to_dir
    contents = contents_of(to_dir)
    index = None

def parent_of(dir):
    return "/".join(dir.split("/")[:-1]) or "/"

def joined(dir1, dir2):
    prefix = dir1 if dir1 == "/" else f"{dir1}/"
    return f"{prefix}{dir2}"

def contents_of(dir):
    return sorted(os.ilistdir(dir), key=lambda x: x[NAME])


class Draw:
    @staticmethod
    def background():
        screen.brush = brushes.color(0, 0, 0)
        screen.draw(shapes.rectangle(0, 0, 160, 120))

    @staticmethod
    def title():
        screen.brush = brushes.color(0, 255, 0)
        screen.font = large_font
        screen.text("File System", 5, 5)

    @staticmethod
    def breadcrumb(path):
        screen.brush = brushes.color(100, 100, 100)
        screen.font = small_font
        screen.text(path, 5, 20)

    @staticmethod
    def contents(items, current_index=None):
        for i, item in enumerate(items):
            if i >= 8:
                break  # Limit to first 8 items for display
            Draw.item(item, i, is_selected=(i == current_index))

    @staticmethod
    def item(item, index, is_selected=False):
        if is_selected:
            screen.brush = brushes.color(0, 50, 0)
            screen.draw(shapes.rectangle(0, 35 + index * 10, 160, 12))

        screen.font = small_font
        if item[TYPE] == DIR:
            screen.brush = brushes.color(0, 0, 255)
        else:
            screen.brush = brushes.color(255, 255, 255)
        screen.text(item[NAME], 5, 35 + index * 10)


if __name__ == "__main__":
    run(update)
