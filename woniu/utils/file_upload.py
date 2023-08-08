import json
import re

from minio import Minio


class MinioService:
    def __init__(self):

        self.client = Minio(
            "192.168.5.8:9000",
            access_key="VNQ0BPXW7GFRF230OTJZ",
            secret_key="cLNFKPcL2TYvvMwTstsvtVuDvaf4nMeWlkc88rdO",
            secure=False
        )
        self.name = "config"

    def get_client(self, name=None):
        return self.client

    def set_client(self, ip, access_key, secret_key):
        return Minio(ip, access_key, secret_key)

    def is_exist(self, bucket="config"):
        found = self.client.bucket_exists(bucket)

        if not found:
            print("not found!")
        else:
            print("是否存在bucket:", found)

    def upload(self):
        res = self.client.fput_object(
            bucket_name="config",
            object_name="sources.list",
            file_path="sources.list",
            # content_type="image/jpg",
            # metadata={'Content-Type': 'image/jpg'}

        )
        print(res)
        if res:
            print(res.object_name)
            print(res.location)
            print(res.etag)
            print(res.http_headers)
        return {"objectName", res.object_name}

    def set_policy(self, name="config"):
        policy = {
            "Id": "Policy1599794391088",
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Stmt1599794381153",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::" + name + "/*",
                    "Principal": "*"
                }
            ]
        }

        self.client.set_bucket_policy(name, json.dumps(policy))

    def get_policy(self, name="config"):
        policy = self.client.get_bucket_policy(bucket_name=name)
        print(policy)

    def download(self, name, obj):
        target = self.client.get_object(bucket_name=name, object_name=obj)
        print(target.info())

    def download_save(self, obj, path):
        """
        path: 无需指定文件名
        例如：path=./tmp obj=a.txt, file_path =./tmp/a.txt
        """
        file_path = re.sub(r'(?<=\w$)', '/' + obj, path)
        self.client.fget_object(self.name, obj, file_path)


if __name__ == "__main__":
    minio = MinioService()
    # minio.is_exist()
    # minio.set_policy()
    # minio.upload()
    # minio.get_policy()
    # minio.download("config","sources.list")
    minio.download_save(obj='sources.list', path='./tmp')
