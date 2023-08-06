import base64
import io
import json
from abc import abstractmethod


class StorageInterface:
    @abstractmethod
    def write_bytes(self, content_bytes, key):
        pass

    @abstractmethod
    def write_string(self, content_string, key):
        pass

    @abstractmethod
    def write_file(self, file_path, key):
        pass

    def write_json(self, content_json, key):
        self.write_string(json.dumps(content_json), key)

    def write_base64(self, content_base64, key):
        image_data = base64.b64decode(content_base64)
        image_stream = io.BytesIO(image_data)
        self.write_bytes(image_stream, key)
        # image = Image.open(image_stream)
        # image.tobytes()
        # rnd_number = str(random.randint(100000, 999999))
        # suffix = os.path.splitext(key)[-1].lower().lstrip('.')
        # tmp_image_path = '{}-{}.{}'.format(str(int(time.time())), rnd_number, suffix)
        # image.save(tmp_image_path)
        # self.write_file(tmp_image_path, key)


def create_storage(storage_type):
    if storage_type == "MINIO":
        from taichu_dataflow.storage.alluxio import StorageAlluxio
        return StorageAlluxio()
    elif storage_type == "OBS":
        from taichu_dataflow.storage.obs import StorageObs
        return StorageObs()
