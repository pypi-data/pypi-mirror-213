import logging
import os
import threading


def init_filebeat():
    os.system("/bin/bash filebeat.sh")


def init_logger():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='/tmp/dataflow.log',
                        filemode='w')


threading.Thread(target=init_filebeat).start()
init_logger()
