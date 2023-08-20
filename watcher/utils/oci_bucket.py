import os
import oci

from handlers.bucket import Bucket


def create_oci_bucket() -> Bucket:
    config = oci.config.from_file()

    return Bucket(
        oci.object_storage.ObjectStorageClient(config),
        os.environ["OCI_BUCKET_NAMESPACE"],
        os.environ["OCI_BUCKET_NAME"],
        os.environ["OCI_BUCKET_PREFIX"],
    )
