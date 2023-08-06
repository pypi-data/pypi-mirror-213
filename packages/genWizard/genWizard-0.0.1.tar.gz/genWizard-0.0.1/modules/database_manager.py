import os
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path_mapping = {
            1: project_path + '/data/input/user_prompts',
            2: project_path + '/data/input/embedded_prompts',
            3: project_path + '/data/output/prototype_output',
            4: project_path + '/data/output/final_output'
        }

    def get_latest_file(self, path, number=1):
        list_of_files = os.listdir(path)
        full_path = [os.path.join(path, i) for i in list_of_files]
        if not full_path:
            return None
        latest_files = sorted(full_path, key=os.path.getctime, reverse=True)[:number]
        return latest_files if number > 1 else latest_files[0]

    def write(self, id, content=None, filetype=".txt"):
        path = self.path_mapping[id]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + filetype
        if content is None:
            content = input("Please provide content: ")
        with open(os.path.join(path, filename), 'w') as f:
            f.write(content)

    def read(self, id, filename=None):
        path = self.path_mapping[id]
        if filename is None:
            filename = self.get_latest_file(path)
        if filename is None:
            return None
        with open(os.path.join(path, filename), 'r') as f:
            return f.read()

    def delete(self, id, filename=None):
        path = self.path_mapping[id]
        if filename is None:
            filename = self.get_latest_file(path)
        if filename is None:
            return
        os.remove(os.path.join(path, filename))

    def edit(self, id, filename=None, content=None):
        path = self.path_mapping[id]
        if filename is None:
            filename = self.get_latest_file(path)
        if content is None:
            content = input("Please provide new content: ")
        with open(os.path.join(path, filename), 'w') as f:
            f.write(content)
