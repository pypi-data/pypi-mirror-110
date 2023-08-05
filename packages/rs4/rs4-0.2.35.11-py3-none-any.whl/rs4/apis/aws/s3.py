import boto3
from urllib import parse
from rs4 import pathtool

S3 = boto3.resource ('s3')
def upload (source, target, acl = None):
    parts = parse.urlparse (target) # 's3://roadkore/weights/adsa.h5'
    assert parts.scheme == 's3'
    bucket_name = parts.netloc
    bucket = S3.Bucket(name = bucket_name)
    extra_args = {}
    if acl == 'public':
        extra_args ['ACL'] = 'public-read'
    bucket.upload_file (source, parts.path [1:], ExtraArgs = extra_args)

def download (source, target):
    parts = parse.urlparse (source) # 's3://roadkore/weights/adsa.h5'
    assert parts.scheme == 's3'
    bucket_name = parts.netloc
    bucket = S3.Bucket(name = bucket_name)
    pathtool.mkdir (os.path.dirname (target))
    bucket.download_file (parts.path [1:], target)
