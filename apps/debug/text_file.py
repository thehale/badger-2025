from scroll_list import ScrollList


class TextFileViewer(ScrollList):
    def __init__(self, file_path, on_close=lambda: None):
        super().__init__("", file_path)
        self.content_items = self.load_file(file_path)
        self.on_close = on_close

    def on_button_back(self):
        self.on_close()

    def load_file(self, file_path=None):
        try:
            with open(file_path, "r") as f:
                return f.readlines()
        except Exception as e:
            return [f"Error loading file: {e}"]
