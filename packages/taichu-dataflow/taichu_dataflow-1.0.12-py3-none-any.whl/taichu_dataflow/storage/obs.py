import logging

from taichu_dataflow.storage import StorageInterface
from taichu_dataflow.storage.env import *
from obs import ObsClient, PutObjectHeader


class StorageObs(StorageInterface):
    _client = None
    _bucket = None

    def __init__(self):
        self._bucket = STORAGE_BUCKET
        self._client = ObsClient(
            access_key_id=OBS_ACCESS_KEY_ID,
            secret_access_key=OBS_SECRET_ACCESS_KEY,
            server=OBS_SERVER
        )

    def write_bytes(self, content_bytes, key):
        self.write_string(content_bytes, key)

    def write_string(self, content_string, key):
        try:
            self._client.putContent(self._bucket, key, content=content_string)
        except Exception as e:
            logging.info("key: " + key)
            logging.error("TaichuStorageError", e)

    def write_file(self, file_path, key):
        headers = PutObjectHeader()
        headers.contentType = 'text/plain'
        self._client.putFile(self._bucket, key, file_path, metadata={}, headers=headers)
