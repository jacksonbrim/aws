import logging
import boto3
from botocore.exceptions import ClientError
import argparse

def deleteObject(s3, obj):
    try:
        response = obj.delete()
    except ClientError as e:
        logging.error(e)
        return False
    return response
    
def argParse():
    parser = argparse.ArgumentParser(description="Deletes object from bucket")
    parser.add_argument('bucket', help="Bucket to delete object from")
    parser.add_argument('key', help="Name of object to delete from bucket")
    parser.add_argument('-r', '--response', action="store_true", help="Shows the response of the request to delete the object")
    args = parser.parse_args()

    return args

def evaluateArgs(s3, obj, args):

    response = deleteObject(s3, obj)

    if args.response:
        print(f"Response:\n{response}")

def main():

    args = argParse()

    s3 = boto3.resource('s3')
    obj = s3.Object(args.bucket, args.key)

    evaluateArgs(s3, obj, args)




    
if __name__=="__main__":
    main()
