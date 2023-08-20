import os
import time
import handlers.indexer as indexer
import handlers.bucket as bucket
import utils.file as file
import oci
from dotenv import load_dotenv


def watch(b: bucket.Bucket, i: indexer.Indexer):
    files = b.list_bucket()
    files_to_index = i.get_unindexed_files(files)

    if len(files_to_index) == 0:
        print("No files to index")
        return

    print(f"Indexing {len(files_to_index)} files")

    tmp_file_dir = file.create_tmp_dir(b.prefix)

    b.download_files(files_to_index, tmp_file_dir)
    i.execute(files_to_index, tmp_file_dir)

    file.del_tmp_dir(tmp_file_dir)

    print("Indexing complete")


def main():
    if __name__ == "__main__":
        load_dotenv()

        reconciliation_interval = (
            float(os.environ["RECONCILIATION_INTERVAL_MINUTES"]) * 60
        )

        config = oci.config.from_file()
        oci_client = oci.object_storage.ObjectStorageClient(config)

        b = bucket.Bucket(
            oci_client,
            os.environ["OCI_BUCKET_NAMESPACE"],
            os.environ["OCI_BUCKET_NAME"],
            os.environ["OCI_BUCKET_PREFIX"],
        )

        i = indexer.Indexer(os.environ["INDEX_FILE"])

        while True:
            watch(b, i)
            time.sleep(reconciliation_interval)


main()
