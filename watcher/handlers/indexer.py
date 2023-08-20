import json


class Indexer:
    def __init__(self, indexFile: str):
        self.indexFile = indexFile
        try:
            index = json.load(open(indexFile))
        except FileNotFoundError:
            index = {}

        self.index = index

    def get_unindexed_files(self, files: list[str]) -> list[str]:
        return [file for file in files if file not in self.index]

    def execute(self, files: list[str], tmp_file_dir: str):
        for file in files:
            try:
                self.__index__(f"{tmp_file_dir}/{file}")
            except Exception as e:
                print(f"Failed to index {file}: {e}")
                continue
            self.index[file] = True
        with open(self.indexFile, "w") as f:
            json.dump(self.index, f)
        return

    def __index__(self, filePath: str):
        return
