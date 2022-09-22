import logging
import boto3
from botocore.exceptions import ClientError
import argparse

def downloadFile(obj, filename):
    try:
        with open(filename, 'wb') as data:
            response = obj.download_fileobj(data)
    except ClientError as e:
        logging.error(e)
        return False
    return response 

def argParse():
    parser = argparse.ArgumentParser(description="Downloads object from specified bucket and saves to output")
    parser.add_argument('bucket', help="Bucket to download file from")
    parser.add_argument('key', help="Key value of object to download from s3 bucket")
    parser.add_argument('output', help="Filename to output file to")
    parser.add_argument('-r', '--response', action="store_true", help="Flag to print out the response from the download request")
    args = parser.parse_args()

    return args

def evaluateArgs(s3, args):
    bucket = s3.Bucket(args.bucket)
    obj = bucket.Object(args.key)

    response = downloadFile(obj, args.output)

    if args.response:
        print(f"Response: {response}")

def main():
    # Retrieve the list of existing buckets
    s3 = boto3.resource('s3')
    args = argParse()

    evaluateArgs(s3, args)

    
if __name__=="__main__":
    main()
