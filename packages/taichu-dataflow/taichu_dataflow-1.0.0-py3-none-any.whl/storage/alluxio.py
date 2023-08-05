import logging

from storage.storage import StorageInterface
import boto.s3.connection
import storage.env
import boto.exception


class StorageAlluxio(StorageInterface):
    _client = None
    _bucket = None

    def __init__(self, storage_type):
        self._client = boto.connect_s3(
            aws_access_key_id=storage.env.S3_ACCESS_KEY_ID,
            aws_secret_access_key=storage.env.S3_SECRET_ACCESS_KEY,
            # host='alluxio-master-0.infra',
            host=storage.env.ALLUXIO_HOST,
            port=storage.env.ALLUXIO_PORT,
            path=storage.env.ALLUXIO_PATH,
            is_secure=False,
            calling_format=boto.s3.connection.OrdinaryCallingFormat(),
        )
        self._bucket = self._client.get_bucket(storage.env.STORAGE_BUCKET)

    def write_bytes(self, content_bytes, key):
        pass

    def write_string(self, content_string, key):
        try:
            s3_key = self._bucket.new_key(key)
            s3_key.set_contents_from_string(content_string)
        except boto.exception.BotoClientError:
            pass
        except Exception as e:
            logging.info("key: " + key)
            logging.error("TaichuStorageError", e)
