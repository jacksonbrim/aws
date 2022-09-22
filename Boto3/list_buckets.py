import logging
import boto3
from botocore.exceptions import ClientError
import argparse

def printBuckets(s3):
    try:
        response = s3.list_buckets()
    except ClientError as e:
        logging.error(e)
        return False

    # Output the bucket names
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    return response

def listBuckets(s3):
    try:
        response = s3.list_buckets()
    except ClientError as e:
        logging.error(e)
        return False

   # store the bucket names
    return response

def listObject(s3, bucket):
    # Output the Objects in the bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket, Delimiter='string')
    except ClientError as e:
        logging.error(e)
        return False

    return response

def printObject(s3, bucket):
    try:
        response = listObject(s3, bucket)
    except ClientError as e:
        logging.error(e)
        return False

    # Print the Objects in the bucket
    print(f"Bucket: {bucket}")
    try:
        for item in response['Contents']:
            print(f"\tKey: {item['Key']}")
    except:
        pass


def listAllObjectsInBucket(s3):
    buckets = listBuckets(s3)
    for bucket in buckets['Buckets']:
        print(f"Bucket: {bucket['Name']}")
        try:
            objects = listObject(s3, bucket['Name'])
            for item in objects['Contents']:
                print(f"\tKey: {item['Key']}")
        except:
                pass
def argParse():
    parser = argparse.ArgumentParser(description="Lists S3 Buckets, and / or Objects in S3 Buckets")
    parser.add_argument('-l', dest="list", action='store_true', help="[Default] List the buckets") 
    parser.add_argument('-a', dest="all", action='store_true', help="Lists all Objects in All Buckets")
    parser.add_argument('bucket', nargs='*', help="Lists objects in specified bucket(s)")

    args = parser.parse_intermixed_args()

    return args

def evaluateArgs(s3, args):
    if args.all is True:
        listAllObjectsInBucket(s3)
    elif args.bucket:
        for i in args.bucket:
            printObject(s3, i)
    else:
        printBuckets(s3)


def main():
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
    args = argParse()
    evaluateArgs(s3, args)

    
if __name__=="__main__":
    main()
