import logging
import boto3
from botocore.exceptions import ClientError
import argparse


def delete_bucket(bucket_name):
    """Delete an S3 bucket"""

    # Delete bucket
    try:
        s3_client = boto3.client('s3')
        response = s3_client.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return response 




def argParser():
    """Parse arguments from the command line"""
    parser = argparse.ArgumentParser(
            description='A program that deletes an S3 bucket using your AWS configuration variables')
    parser.add_argument("bucket_name", help="Name of the bucket that you'd like to delete")
    parser.add_argument("-r", "--response", action="store_true", help="Flag to print out response")
    arg = parser.parse_args()
    return arg

def evaluateArgs(args):
    response = delete_bucket(args.bucket_name)

    if args.response:
        print("Response:\n{response}")

def main():
    args = argParser()
    evaluateArgs(args)

if __name__=="__main__":
    main()
