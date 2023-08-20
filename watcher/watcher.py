import os
import time
import numpy as np
from dotenv import load_dotenv
from handlers.indexer import Indexer
from handlers.bucket import Bucket
from utils.file import create_tmp_dir, del_tmp_dir
from utils.oci_bucket import create_oci_bucket
from database.in_memory import InMemoryDB
from model.embedding_model import EmbeddingModel

def watch(bucket: Bucket, indexer: Indexer):
    files = bucket.list_bucket()
    files_to_index = indexer.get_unindexed_files(files)

    if len(files_to_index) == 0:
        print("No files to index")
        return

    print(f"Indexing {len(files_to_index)} files")

    tmp_file_dir = create_tmp_dir(bucket.prefix)

    bucket.download_files(files_to_index, tmp_file_dir)
    indexer.execute(files_to_index, tmp_file_dir)

    del_tmp_dir(tmp_file_dir)

    print("Indexing complete")


def main():
    if __name__ == "__main__":
        load_dotenv()

        db = InMemoryDB("./tmp/data.csv")

        reconciliation_interval = (
            float(os.environ["RECONCILIATION_INTERVAL_MINUTES"]) * 60
        )

        bucket = create_oci_bucket()

        indexer = Indexer(os.environ["INDEX_FILE"], db)

        while True:
            watch(bucket, indexer)
            print(db.get())
            time.sleep(reconciliation_interval)
main()
