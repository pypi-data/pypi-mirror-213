from ns_lab_aws.config.libraries import load_dotenv
from ns_lab_aws.config.libraries import os
from ns_lab_aws.config.libraries import boto3  
from ns_lab_aws.config.libraries import logging, logging_config, colorlog
from ns_lab_aws.config.libraries import Console, Table, box
from ns_lab_aws.config.libraries import argparse


# Setting-1: Load environment variables
load_env = load_dotenv(dotenv_path='.env')


# Setting-2: Load AWS credentials and create AWS Session
aws_access  = os.getenv('AWS_KEY')
aws_secret  = os.getenv('AWS_SECRET')
aws_region  = os.getenv('AWS_REGION')
aws_params  = {
    'aws_access_key_id':     aws_access,
    'aws_secret_access_key': aws_secret,
    'region_name':           aws_region
}

aws_session = boto3.Session(**aws_params)


# Setting-3: Logging
logging_config.fileConfig('logging.conf')
logger = logging


# Setting-4: Tables
console = Console()
#           Table-4.1: Show list of buckets
table_buckets = Table(title='\nAWS S3 Buckets', show_header=True, header_style="bold magenta", box=box.SIMPLE)
table_buckets.add_column("ID",       justify="center", style="dim")
table_buckets.add_column("Files",    justify="right")
table_buckets.add_column("Bucket",   justify="left")
table_buckets.add_column("Location", justify="left")
table_buckets.add_column("Created",  justify="center")

#           Table-4.2: Show list of files in a bucket
table_files = Table(title='\nFiles in AWS S3 Bucket', show_header=True, header_style="bold magenta", box=box.SIMPLE)
table_files.add_column("ID",        justify="center", style="dim",  width=4)
table_files.add_column("Path",      justify="left",   style="dim")
table_files.add_column("File",      justify="left")
table_files.add_column("Extension", justify="left")
table_files.add_column("Size",      justify="right")
table_files.add_column("Created",   justify="center")


# Setting-5: ArgParse
s3_parser = argparse.ArgumentParser(description='AWS S3 Buckets')
s3_parser.add_argument('--list',     action='store_true', help='List all buckets')
s3_parser.add_argument('--create',   action='store_true', help='Create bucket')
s3_parser.add_argument('--delete',   action='store_true', help='Delete bucket')
s3_parser.add_argument('--upload',   action='store_true', help='Upload file to bucket')
s3_parser.add_argument('--download', action='store_true', help='Download file from bucket')
s3_parser.add_argument('--content',  action='store_true', help='Show bucket content')
s3_parser.add_argument('--force',    action='store_true', help='Force delete bucket')
s3_parser.add_argument('-b', '--bucket', type=str, help='Bucket name')
s3_parser.add_argument('-f', '--file',   type=str, help='File name')
s3_parser.add_argument('-d', '--dir',    type=str, help='Directory name')

