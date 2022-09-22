import logging
import boto3
from botocore.exceptions import ClientError
import argparse

def uploadObject(s3, bucket, key, file):
    try:
        response = s3.Object(bucket, key).upload_file(file.name)
    except ClientError as e:
        logging.error(e)
        return False
    return response
    
def argParse():
    parser = argparse.ArgumentParser(description="Puts object to specified bucket")
    parser.add_argument('bucket', help="Bucket to put object in")
    parser.add_argument('key', help="Name to assign newly put object")
    parser.add_argument('file', type=argparse.FileType('r'), help="File to put in s3 bucket")
    parser.add_argument('-r', '--response', action="store_true", help="Flag to print out response from the upload request")
    args = parser.parse_args()

    return args

def evaluateArgs(s3, args):

    response = uploadObject(s3, args.bucket, args.key, args.file)

    if args.response:
        print(f"Response: {response}")

def main():

    s3 = boto3.resource('s3')
    args = argParse()
    evaluateArgs(s3, args)


    
if __name__=="__main__":
    main()
