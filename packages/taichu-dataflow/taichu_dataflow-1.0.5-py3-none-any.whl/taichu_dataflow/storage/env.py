import os

# 必填项目
STORAGE_TYPE = os.getenv('STORAGE_MEDIA', 'MINIO')

STORAGE_BUCKET = os.getenv('STORAGE_BUCKET', 'publish-data')

ALLUXIO_HOST = os.getenv('ALLUXIO_HOST', 'alluxio-proxy.infra')
ALLUXIO_PORT = os.getenv('ALLUXIO_PORT', 39999)
ALLUXIO_PATH = os.getenv('ALLUXIO_PORT', '/api/v1/s3')
S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', 'Credential=root/')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', '')
