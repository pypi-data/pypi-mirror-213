import json
class FileLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, 'r', encoding="utf-8") as f:
            return f.read()

class JsonFileLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, 'r', newline='', encoding="utf-8") as f:
            return json.load(f)

class LabelStudioLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, 'r', encoding="utf-8") as f:
            return f.read()