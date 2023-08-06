from .logger import Logger

import boto3
from botocore.exceptions import ClientError


class AWSAdapter:
    def __init__(self, logger: Logger):
        self.logger = logger

    def upload_file_to_s3(self, region, bucket_name, file_path, file_key):
        try:
            self.logger.info(f"Uploading file {file_path} to Bucket (region: {region}): {bucket_name} -> {file_key}")
            s3_resource = boto3.resource("s3", region_name=region)
            s3_resource.Bucket(bucket_name).upload_file(file_path, file_key)
            self.logger.info(f"File {file_path} uploaded")
        except ClientError as e:
            self.logger.error(
                f"Error uploading file {file_path} to Bucket: {bucket_name} -> {file_key}: {e.response['Error']['Message']}"
            )
