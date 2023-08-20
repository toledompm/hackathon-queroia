import oci


class Bucket:
    def __init__(
        self,
        cli: oci.object_storage.ObjectStorageClient,
        bucket_namespace: str,
        bucket_name: str,
        prefix: str,
    ) -> None:
        self.cli = cli
        self.namespace = bucket_namespace
        self.name = bucket_name
        self.prefix = prefix

    def list_bucket(self) -> list[str]:
        """
        list_bucket returns a list of all files in the bucket
        """
        all_files = self.cli.list_objects(self.namespace, self.name, prefix=self.prefix)

        return [obj.name for obj in all_files.data.objects]

    def download_files(self, files: list[str], tmp_file_dir: str) -> None:
        """
        download_files downloads a list of files from the bucket to a temporary directory
        """
        for file in files:
            response = self.cli.get_object(self.namespace, self.name, file)
            with open(f"{tmp_file_dir}/{file}", "wb") as f:
                for chunk in response.data.raw.stream(
                    1024 * 1024, decode_content=False
                ):
                    f.write(chunk)
        return

    def upload_file(self, file_name: str, file_content: bytes) -> None:
        """
        upload_file uploads a file to the bucket
        """
        file_path = f"{self.prefix}/{file_name}"
        self.cli.put_object(self.namespace, self.name, file_path, file_content)
        return
