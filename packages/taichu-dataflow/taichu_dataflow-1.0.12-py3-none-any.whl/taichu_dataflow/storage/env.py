import os
import uuid

# 必填项目
STORAGE_TYPE = os.getenv('STORAGE_MEDIA', 'MINIO')

STORAGE_BUCKET = os.getenv('STORAGE_BUCKET', 'publish-data')
SERVICE_NAME = os.getenv('SERVICE_NAME', 'anonymous')

ALLUXIO_HOST = os.getenv('ALLUXIO_HOST', 'alluxio-proxy.infra')
ALLUXIO_PORT = int(os.getenv('ALLUXIO_PORT', 39999))
ALLUXIO_PATH = os.getenv('ALLUXIO_PATH', '/api/v1/s3')
S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', 'Credential=root/')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', '')

OBS_SERVER = os.getenv('OBS_SERVER')
OBS_ACCESS_KEY_ID = os.getenv('OBS_ACCESS_KEY_ID')
OBS_SECRET_ACCESS_KEY = os.getenv('OBS_SECRET_ACCESS_KEY')

service_name = None


def get_service_name():
    global service_name
    if service_name is None:
        env_sn = os.getenv('SERVICE_NAME', 'anonymous')
        if env_sn == 'anonymous':
            service_name = gen_random_name()
            return service_name
        else:
            service_name = env_sn
            return service_name
    else:
        return service_name


def gen_random_name():
    return str(uuid.uuid4()).replace('-', '')[:8]
