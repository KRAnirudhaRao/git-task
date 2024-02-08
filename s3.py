import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    bucket_name = 'anitasmaking'
    region='ap-south-1'
    if region is None:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint' :region}
        s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    return { }
