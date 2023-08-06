from abc import abstractmethod


class StorageInterface:
    @abstractmethod
    def write_bytes(self, content_bytes, key):
        pass

    @abstractmethod
    def write_string(self, content_string, key):
        pass


def create_storage(storage_type):
    if storage_type == "MINIO":
        from storage.alluxio import StorageAlluxio
        return StorageAlluxio(storage_type)
