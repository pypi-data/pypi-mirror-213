from ns_lab_aws.console.client import S3Client 
from ns_lab_aws.config.settings import logger, s3_parser


s3_client = S3Client()


args        = s3_parser.parse_args()
s3_list     = args.list
s3_create   = args.create
s3_delete   = args.delete
s3_bucket   = args.bucket
s3_force    = args.force
s3_content  = args.content
s3_file     = args.file


if s3_list:    
    s3_client.s3_bucket_list()

if s3_delete:
    s3_client.s3_bucket_delete(s3_bucket, s3_force)

if s3_content:
    s3_client.s3_bucket_content(s3_bucket)

if s3_create:
    s3_client.s3_bucket_create(s3_bucket)

if s3_file:
    s3_client.s3_bucket_upload(s3_bucket, s3_file)





