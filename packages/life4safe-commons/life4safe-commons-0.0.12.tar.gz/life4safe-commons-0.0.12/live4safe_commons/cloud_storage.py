from os import getenv
from google.cloud import storage
from azure.storage.blob import BlobServiceClient, ContentSettings, __version__
from azure.core import exceptions
from live4safe_commons.logger_app import get_logger

LOGGER = get_logger("cloud_storage")
CLOUD_STORAGE_TYPE = getenv("CLOUD_STORAGE_TYPE", "AZURE")  # ['GCP', 'AZURE']
STORAGE_PATH = getenv("STORAGE_PATH", "liveness-dev/videos/")
BUCKET_NAME = getenv("BUCKET_NAME", "novaweb-storage")
AZURE_STORAGE_CONNECTION_STRING = getenv('AZURE_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_ACCOUNT = getenv('AZURE_STORAGE_ACCOUNT', "sainovacao")


class CloudStorage:
    def upload_blob(
        self,
        source_file_name,
        destination_blob_name: str,
        blob_type: str,
    ):
        pass

    def delete_blob(self, blob_name: str):
        pass

    def get_url_prefix(self) -> str:
        pass


class GoogleStorage(CloudStorage):
    def __init__(self) -> None:
        super().__init__()
        self.storage_path = STORAGE_PATH
        self.bucket_name = BUCKET_NAME

    def upload_blob(
        self,
        source_file_name,
        destination_blob_name: str,
        blob_type: str = "video/mp4",
    ):
        """Uploads a file to the bucket."""

        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(STORAGE_PATH + destination_blob_name)

        # blob.upload_from_filename(source_file_name)
        blob.upload_from_file(source_file_name, content_type=blob_type)

        LOGGER.info(
            "File {} uploaded to {}.".format(
                source_file_name, STORAGE_PATH + destination_blob_name
            )
        )

    def delete_blob(self, blob_name: str):
        """Deletes a blob from the bucket."""
        blob_name = blob_name.replace(
            "https://storage.googleapis.com/" + self.bucket_name + "/", ""
        )

        storage_client = storage.Client()

        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        blob.delete()

        LOGGER.info("Blob {} deleted.".format(blob_name))

    def get_url_prefix(self) -> str:
        return (
            "https://storage.googleapis.com/"
            + self.bucket_name
            + "/"
            + self.storage_path
            if self.storage_path.endswith("/")
            else self.storage_path + "/"
        )


class AzureStorage(CloudStorage):
    def __init__(self) -> None:
        super().__init__()
        try:
            LOGGER.info("Azure Blob Storage v" + __version__)

            # Create the BlobServiceClient object which
            # will be used to create a container client
            self.blob_service_client = BlobServiceClient.from_connection_string(
                AZURE_STORAGE_CONNECTION_STRING)

            # Create the container
            self.container_client = self.blob_service_client.create_container(
                BUCKET_NAME)

        except exceptions.ResourceExistsError as ex:
            LOGGER.info(
                f"Container '{BUCKET_NAME}' already exists. Exception: {ex}")

        except Exception as ex:
            LOGGER.exception(f'General exception when create bucket: {ex}')

    def upload_blob(
        self,
        source_file_name,
        destination_blob_name: str,
        blob_type: str,
    ):
        # Create a blob client using the
        # local file name as the name for the blob
        blob_client = self.blob_service_client.get_blob_client(
            container=BUCKET_NAME, blob=destination_blob_name)

        # Upload the created file
        content_settings = ContentSettings(content_type=blob_type)
        blob_client.upload_blob(source_file_name.read(),
                                content_settings=content_settings)

        LOGGER.info(
            "File {} uploaded to container {}: {}".format(
                source_file_name, BUCKET_NAME, destination_blob_name
            )
        )

    def delete_blob(self, blob_name: str):
        blob_name = blob_name.replace(
            self.get_url_prefix(), ""
        )

        # Create a blob client using the
        # local file name as the name for the blob
        blob_client = self.blob_service_client.get_blob_client(
            container=BUCKET_NAME, blob=blob_name)

        # Delete the file
        blob_client.delete_blob()

        LOGGER.info("Blob {} deleted.".format(blob_name))

    def get_url_prefix(self) -> str:
        return (
            f"https://{AZURE_STORAGE_ACCOUNT}." +
            "blob.core.windows.net/{BUCKET_NAME}/"
        )


def get_storage():
    if CLOUD_STORAGE_TYPE == "GCP":
        return GoogleStorage()
    elif CLOUD_STORAGE_TYPE == "AZURE":
        return AzureStorage()
    else:
        LOGGER.critical(
            f"CLOUD_STORAGE_TYPE not recognized: {CLOUD_STORAGE_TYPE}"
        )
        raise Exception("CLOUD_STORAGE_TYPE not recognized")
