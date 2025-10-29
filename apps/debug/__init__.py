import sys
import os

sys.path.insert(0, "/system/apps/debug")
os.chdir("/system/apps/debug")

from file_list import FileList
from text_file import TextFileViewer

stack = []

########################################################################################

stack.append(
    FileList(
        open_action=lambda file_path: stack.append(
            TextFileViewer(file_path, on_close=lambda: stack.pop())
        )
    )
)


def update():
    stack[-1].update()
