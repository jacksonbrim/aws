import logging
import boto3
from botocore.exceptions import ClientError
import argparse


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            response =s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False

    return response 




def argParser():
    parser = argparse.ArgumentParser(
            description='A program that creates an S3 bucket using your AWS configuration variables')
    parser.add_argument("bucket_name", help="Name of the bucket that you'd like to create")
    parser.add_argument("-r", "--response", action="store_true", help="Flag to print out response from the create bucket request")
    arg = parser.parse_args()
    return arg

def evalArgs(args):
    response = create_bucket(args.bucket_name)
    if args.response:
        print(f"Response: {response}")

def main():
    args = argParser()

    evalArgs(args)

if __name__=="__main__":
    main()
