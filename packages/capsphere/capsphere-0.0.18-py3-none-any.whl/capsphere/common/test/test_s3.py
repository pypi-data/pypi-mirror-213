import unittest
import boto3
from capsphere.common.s3 import get_total_objects


class TestS3(unittest.TestCase):
    pass
    # session = boto3.Session()
    # s3 = session.resource('s3')
    # src_bucket = s3.Bucket('capsphere-ocr-input')
    #
    # def test_s3_resource(self):
    #     print(get_total_objects(self.src_bucket))
