import json

from model.embedding_model import EmbeddingModel

from database.in_memory import InMemoryDB
import traceback

import utils.transcriptor as transcriptor


class Indexer:
    def __init__(
        self, indexFile: str, db: InMemoryDB, embeddingModel: EmbeddingModel
    ) -> None:
        """
        Indexer is the class that handles file indexing.
        It keeps track of which files have been indexed in a json file, and only indexes files that are not in the index.
        """
        self.indexFile = indexFile
        self.embeddingModdel = embeddingModel
        self.db = db
        try:
            index = json.load(open(indexFile))
        except FileNotFoundError:
            index = {}

        self.index = index

    def get_unindexed_files(self, files: list[str]) -> list[str]:
        """
        get_unindexed_files returns a list of files that are not in the index
        """
        return [file for file in files if file not in self.index]

    def execute(self, files: list[str], tmp_file_dir: str) -> None:
        """
        execute indexes a list of files, adding them to the index
        """
        for file in files:
            try:
                self.__index__(f"{tmp_file_dir}/{file}")
            except Exception as e:
                print(f"Failed to index {file}: {e}")
                traceback.print_exc()
                continue
            self.index[file] = True
        with open(self.indexFile, "w") as f:
            json.dump(self.index, f)
        return

    def __index__(self, filePath: str) -> None:
        if filePath.endswith(".mp4"):
            mp3_path = transcriptor.convert_mp4_to_mp3(filePath)
            transcript = transcriptor.transcription_mp3_to_text(mp3_path)
        elif filePath.endswith(".txt"):
            transcript = transcriptor.parser_text(filePath)
        else:
            return
        transcript["embedding"] = transcript.text.apply(
            self.embeddingModdel.get_embedding
        )
        self.db.insert(transcript)
        return
