import logging
import os.path
import random
import threading
import time

from storage import create_storage
from datetime import datetime
from env import STORAGE_TYPE

storage_mgr = create_storage(STORAGE_TYPE)
storage_prefix = 'sys/export_back/' + os.getenv('SERVICE_NAME', 'anonymous')


def gen_path(suffix=''):
    suffix = suffix.lower().lstrip('.')
    date_string = datetime.now().strftime("%Y-%m-%d")
    rnd_number = str(random.randint(100000, 999999))
    # 服务下可以根据类型细分
    return os.path.join(
        storage_prefix,
        date_string,
        '{}-{}.{}'.format(str(int(time.time())), rnd_number, suffix))


def export_back_string(content, suffix='.jpg'):
    threading.Thread(target=_export_back_string_async, args=(content, suffix)).start()


def export_back_file(path_to_file):
    suffix = os.path.splitext(path_to_file)[-1].lower()
    threading.Thread(target=_export_back_file_async, args=(path_to_file, suffix)).start()


def _logfmt(suffix, key):
    logging.info({
        'suffix': suffix,
        'key': key
    })
    logging.info({
        "id": "da116e7b-dee7-4395-bac2-65813334b03a",
        "app_name": "aigc-backend",
        "create_time": "2023-06-12 15:52:12",
        "user_id": "1889531xx35",
        "action": "export_back",
        "action_params": {
            "suffix": suffix,
            "key": key
        }
    })


def _export_back_file_async(path_to_file, suffix):
    key = gen_path(suffix)
    storage_mgr.write_file(path_to_file, key)
    _logfmt(suffix, key)


def _export_back_string_async(content, suffix='.jpg'):
    key = gen_path(suffix)
    storage_mgr.write_string(content, key)
    _logfmt(suffix, key)


# def suffix_to_type(suffix):
#     file_types = {
#         "txt": "text",
#         "jpg": "image",
#         "png": "image",
#     }

if __name__ == "__main__":
    export_back_string('abc')
