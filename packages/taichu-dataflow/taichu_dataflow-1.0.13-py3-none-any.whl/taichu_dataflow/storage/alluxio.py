import logging

from taichu_dataflow.storage import StorageInterface
import boto.s3.connection
from taichu_dataflow.storage.env import *
import boto.exception


class StorageAlluxio(StorageInterface):
    _client = None
    _bucket = None

    def __init__(self):
        self._client = boto.connect_s3(
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
            host=ALLUXIO_HOST,
            port=ALLUXIO_PORT,
            path=ALLUXIO_PATH,
            is_secure=False,
            calling_format=boto.s3.connection.OrdinaryCallingFormat(),
        )
        self._bucket = self._client.get_bucket(STORAGE_BUCKET)

    def write_bytes(self, content_bytes, key):
        try:
            s3_key = self._bucket.new_key(key)
            s3_key.set_contents_from_file(content_bytes)
        except boto.exception.BotoClientError:
            pass
        except Exception as e:
            logging.info("key: " + key)
            logging.error("TaichuStorageError", e)

    def write_string(self, content_string, key):
        try:
            s3_key = self._bucket.new_key(key)
            s3_key.set_contents_from_string(content_string)
        except boto.exception.BotoClientError:
            pass
        except Exception as e:
            logging.info("key: " + key)
            logging.error("TaichuStorageError", e)

    def write_file(self, file_path, key):
        s3_key = self._bucket.new_key(key)
        with open(file_path, "rb") as f:
            try:
                s3_key.set_contents_from_file(f)
            except:
                return