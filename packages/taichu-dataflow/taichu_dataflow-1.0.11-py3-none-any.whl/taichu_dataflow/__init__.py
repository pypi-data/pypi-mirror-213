import logging
import os
import threading


def init_filebeat():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'filebeat.sh')
    os.system(f"/bin/bash {script_path} >/dev/null 2>&1")


def init_logger():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='/tmp/dataflow.log',
                        filemode='a')

threading.Thread(target=init_filebeat).start()
init_logger()
