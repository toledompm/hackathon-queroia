from handlers.bucket import Bucket
from handlers.indexer import Indexer
from utils.file import create_tmp_dir, del_tmp_dir


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
