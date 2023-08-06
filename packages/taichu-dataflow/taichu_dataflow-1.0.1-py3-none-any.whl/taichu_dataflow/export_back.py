import logging
import os.path
import random
import threading
import time

from storage.storage import create_storage
from datetime import datetime
from storage.env import STORAGE_TYPE

storage_mgr = create_storage(STORAGE_TYPE)
storage_prefix = 'sys/export_back/' + os.getenv('SERVICE_NAME', 'anonymous')


def gen_path(suffix=''):
    date_string = datetime.now().strftime("%Y-%m-%d")
    rnd_number = str(random.randint(100000, 999999))
    return os.path.join(
        storage_prefix,
        date_string,
        '{}-{}.{}'.format(str(int(time.time())), rnd_number, suffix.lstrip('.')))


def export_back_base64_image(content, suffix='.jpg'):
    threading.Thread(target=_export_back_base64_image_async, args=(content, suffix)).start()


def _export_back_base64_image_async(content, suffix='.jpg'):
    key = gen_path(suffix)
    storage_mgr.write_string(content, key)
    logging.info({
        'export_back_type': 'image',
        'key': key
    })


if __name__ == "__main__":
    export_back_base64_image('abc')
