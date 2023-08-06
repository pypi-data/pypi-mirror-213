import logging
import os.path
import random
import threading
import time
import uuid

from taichu_dataflow.storage import create_storage
from datetime import datetime
from taichu_dataflow.storage.env import STORAGE_TYPE, get_service_name

storage_mgr = create_storage(STORAGE_TYPE)
storage_prefix = 'sys/export_back/' + os.getenv('SERVICE_NAME', 'anonymous')

__all__ = [
    'export_back', 'export_back_base64', 'export_back_json',
    'export_back_bytes', 'export_back_string', 'export_back_file'
]


def gen_path(suffix=''):
    suffix = suffix.lower().lstrip('.')
    date_string = datetime.now().strftime("%Y-%m-%d")
    rnd_number = str(random.randint(100000, 999999))
    # 服务下可以根据类型细分
    return os.path.join(
        storage_prefix,
        date_string,
        '{}-{}.{}'.format(str(int(time.time())), rnd_number, suffix))


# 通用回流函数
def export_back(export_type, content, suffix=''):
    threading.Thread(target=_export_back_async, args=(export_type, content, suffix)).start()


def _export_back_async(export_type, content, suffix):
    key = gen_path(suffix)
    func = getattr(storage_mgr, 'write_' + export_type)
    func(content, key)


# 以下为辅助函数
def export_back_base64(content, suffix):
    _export_back_async('base64', content, suffix)


def export_back_bytes(content, suffix):
    _export_back_async('bytes', content, suffix)


def export_back_string(content, suffix):
    _export_back_async('string', content, suffix)


def export_back_json(content):
    _export_back_async('json', content, 'json')


def export_back_file(path_to_file):
    suffix = os.path.splitext(path_to_file)[-1].lower()
    _export_back_async('file', path_to_file, suffix)


def _logfmt(suffix, key):
    logging.info({
        "id": str(uuid.uuid4()),
        "app_name": get_service_name(),
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        # "user_id": "1889531xx35",
        "action": "export_back",
        "action_params": {
            "suffix": suffix,
            "key": key
        }
    })


if __name__ == "__main__":
    # export_back_string('abc')
    # global base64_string
    # export_back('string', 'abc', 'txt')
    # export_back('json', {'abc': 123}, 'json')
    # export_back('base64', base64_string, 'jpg')
    export_back('file', '123.xyz', 'xyz')
