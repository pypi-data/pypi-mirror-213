
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from cloudservices.config import cloud_config
from libcloud.common.google import GoogleAuthType

ACL = ["public-read", "private", "public-read-write",
       "authenticated-read", "bucket-owner-read", "bucket-owner-full-control"]


class Storage:
    """
    Initializes Storage class with specified bucket name.

    Args:
        bucket_name (str): The name of the bucket to interact with.

    Returns:
        None : The appropriate storage client instance is initialized.

    Examples:
    ---------
    Initialize a `Storage` instance for interacting with an AWS S3 bucket named 'my-bucket':
    ```
    storage = Storage(bucket_name='my-bucket')
    ```

    Initialize a `Storage` instance for interacting with a GCP GCS bucket named 'my-bucket':
    ```
    storage = Storage(bucket_name='my-bucket')
    ```
    """

    def __init__(self, bucket_name):

        cloud_provider = cloud_config.cloud_provider

        driver = None
        try:
            if cloud_provider == 'AWS':
                # Set up the driver for AWS S3
                aws_cls = get_driver(Provider.S3)
                aws_driver = aws_cls(
                    key=cloud_config.aws_access_key_id, secret=cloud_config.aws_secret_access_key, region=cloud_config.aws_region)
                driver = aws_driver
            elif cloud_provider == 'GCP':
                # Set up the driver for GCP GCS
                if cloud_config.gcp_token_source == "custom":
                    gcp_cls = get_driver(Provider.GOOGLE_STORAGE)
                    gcp_credentials = cloud_config.gcp_service_account_key_json or {}
                    gcp_driver = gcp_cls(
                        key=gcp_credentials['client_email'], secret=gcp_credentials['private_key'])
                    driver = gcp_driver
                else:
                    gcp_cls = get_driver(Provider.GOOGLE_STORAGE)
                    driver = gcp_cls(auth_type=GoogleAuthType.GCE, key='-')
            else:
                raise ValueError(
                    f"Unsupported cloud provider: {cloud_provider}")

            container = driver.get_container(container_name=bucket_name)

            self.container = container
            self.bucket_name = bucket_name
            self.driver = driver
        except Exception as e:
            raise Exception("Error in Storage: {}".format(e))

    def upload(self, src_path, dest_path, acl=None, cache_control=None, content_type=None):
        """
        Uploads a file to the specified bucket.

        Args:
            src_path (str): The path of the file to upload.
            dest_path (str): The path to upload the file to.

        Returns:
            None
        """
        try:
            extra = {}
            headers = {}
            if acl:
                if acl not in ACL:
                    raise ValueError(f"Invalid ACL: {acl}")
                # Set the ACL for the uploaded file
                extra['acl'] = acl
            if cache_control is not None:
                # Set the Cache-Control for the uploaded file
                headers['Cache-Control'] = cache_control
            if content_type is not None:
                # Set the Content-Type for the uploaded file
                extra['content_type'] = content_type

            with open(src_path, "rb") as iterator:
                obj = self.driver.upload_object_via_stream(
                    iterator=iterator, container=self.container, object_name=dest_path, extra=extra, headers=headers
                )
                if not obj:
                    raise Exception("Error uploading object : {}, to bucket: {}".format(
                        src_path, self.bucket_name))
        except Exception as e:
            raise Exception("Error uploading file: {}".format(e))

    def download(self, src_path, dest_path):
        """
        Downloads a file from the specified bucket.

        Args:
            src_path (str): The path of the file to download.
            dest_path (str): The path to download the file to.

        Returns:
            None
        """
        try:
            obj = self.driver.get_object(self.bucket_name, src_path)
            result = obj.download(destination_path=dest_path)
            if not result:
                raise Exception("Error downloading object : {}, from bucket: {}".format(
                    src_path, self.bucket_name))
        except Exception as e:
            raise Exception("Error downloading file: {}".format(e))

    def delete(self, path):
        """
        Deletes a file from the specified bucket.

        Args:
            path (str): The path of the file to delete.

        Returns:
            None
        """
        try:
            obj = self.driver.get_object(self.bucket_name, path)
            result = obj.delete()
            if not result:
                raise Exception("Error deleting object : {}, from bucket: {}".format(
                    path, self.bucket_name))
        except Exception as e:
            raise Exception("Error deleting file: {}".format(e))
