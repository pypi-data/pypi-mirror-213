import boto3
import botocore
import os
import sys
import yaml

class Functions:
    """ Helper functions for interacting with AWS"""


    def parse_yaml(file):
        """Exposes configuration YAML file

        Args:
            file (.yml): Config

        Returns:
            dict: access like yml_filename['aws']['our_bucket'] 
        """
        try: 
            with open(file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f'{e}\nDid you create the config file described in the README?')
            sys.exit(1)


    def connect_to_s3():
        """Connect to S3 resource using boto3

        Returns:
            boto3 resource: boto3 S3 resource
        """
        try:
            return boto3.resource("s3")
        except Exception as e:
            print(f"Can't connect to S3. Error: {e}")
            sys.exit(1)


    def assure_s3_bucket(s3, bckt):
        """Check if bucket exists and create if not

        Args:
            s3 (boto3 resource): boto3 S3 resource
            bckt (S3 bucket): S3 bucket
        """
        try:
            s3.meta.client.head_bucket(Bucket = bckt)
            print('Specified bucket exists')
        except botocore.exceptions.ClientError as e:
            print(f'Error code: {e}')
            if e.response["Error"]["Code"] == "404":
                print ('Bucket failed head_bucket() call, likely does not exist')
                s3.create_bucket(Bucket = bckt)
                print(f'Created {bckt}')


    def diff_bucket_objs(s3, bucket_1, prefix_1, bucket_2, prefix_2, match_extensions=False):
        """Identifies the objects in bucket_1 that are not in bucket_2 by key including prefix and extension

        Args:
            s3 (boto3 resource): boto3 S3 resource
            bucket_1 (S3 bucket): 1st S3 bucket
            prefix_1 (String): prefix for objects in bucket 1
            bucket_2 (S3 bucket): 2nd S3 bucket
            prefix_2 (String): prefix for objects in bucket 2
            match_extensions (bool): Flag to consider matching file extensions (default: False)

        Returns:
            set: diff in bucket contents
        """
        def process_objects(bucket, prefix):    
        # returns the set of keys after applying the prefix and optionally removing file extensions.
            keys = set()
            for obj in bucket.objects.filter(Prefix=prefix):
                key = obj.key[len(prefix):] if prefix else obj.key
                if not match_extensions:
                    key = os.path.splitext(key)[0]
                keys.add(key)
            return keys

        bucket_1_keys = process_objects(s3.Bucket(bucket_1), prefix_1)
        bucket_2_keys = process_objects(s3.Bucket(bucket_2), prefix_2)

        diff = bucket_1_keys.difference(bucket_2_keys)
        print(f'There were {len(diff)} objects missing')
        return diff


    def copy_over_all_objects(s3, source, source_prefix, dest, dest_prefix, objects):
        """Copy all prefixed objects from AWS S3 bucket to another

        Args:
            s3 (boto3 resource): boto3 S3 resource
            source (S3 bucket): source S3 bucket
            source_prefix (String): prefix for objects in source
            dest (S3 bucket): destination S3 bucket
            dest_prefix (String): prefix for objects in destination
            objects (list): objects to copy between buckets
        """
        key_dicts = [{'Bucket': source, 'Key': f'{source_prefix}{key}'} for key in objects]
        destination_keys = [f'{dest_prefix}{key}' for key in objects]
        
        results = list(map(lambda key_dict, dest_key: s3.Bucket(dest).copy(key_dict, dest_key), key_dicts, destination_keys))
        ct = len(results)
        
        for key, result in zip(objects, results):
            if result['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f'Copied over: {key}')
        
        print(f'Copying complete, {dest_prefix} folder on destination bucket updated. {ct} objects copied over.')


    def search_s3_bucket_contents(s3_client, bucket_name, search_term):
        """Searches for a given search term in the contents of an S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket to search.
            search_term (str): The term to search for in the bucket contents.

        """
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        for obj in response.get('Contents', []):
            object_key = obj['Key']
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            content = response['Body'].read().decode('utf-8')  # Assuming text content, adjust decoding based on content type

            if search_term in content:
                print(f"Found '{search_term}' in object: {object_key}")
                break

