from ns_lab_aws.services.s3buckets import S3Buckets
from ns_lab_aws.config.settings import table_buckets, table_files, console
from ns_lab_aws.config.settings import s3_parser
from ns_lab_aws.config.settings import logger
from rich import print

from rich.tree import Tree


# logger = logger.getLogger(__name__)
logger = logger.getLogger('NS_CONSOLE:Client')



class S3Client:
    def __init__(self):
        self.s3_buckets = S3Buckets()

    def s3_bucket_list(self) -> None:
        '''List all buckets in S3'''

        all_buckets  = self.s3_buckets.list_buckets()
        bucket_count = 0

        if all_buckets is False:
            logger.debug('Job finished with error')
            return
        
        if len(all_buckets) == 0:
            print('No buckets found')
            return

        for one_bucket in all_buckets:
            bucket_count  += 1
            bucket_name    = one_bucket['bucket']
            backet_created = one_bucket['created']
            bucket_region  = one_bucket['location']
            content_count  = one_bucket['content']
            
            row = [
                str(bucket_count), 
                content_count, 
                bucket_name, 
                bucket_region, 
                backet_created
                ]
            table_buckets.add_row(*row)

        console.print(table_buckets)

    def s3_bucket_delete(self, bucket_name, force):
        '''IN-PROGRESS: Delete bucket'''
        log_header = 'Deleting:'

        result = self.s3_buckets.delete_bucket(bucket_name, force)

        if result:
            logger.info(f'{log_header} The deletion of bucket "{bucket_name}" was successful;')
        else:
            logger.error(f'{log_header} The job finished with error;')

    def s3_bucket_content(self, bucket_name):
        data = self.s3_buckets.content_bucket(bucket_name)

        if data is False:
            logger.error(f'Bucket {bucket_name} not found')
            return
        
        if data is None:
            logger.info(f'Bucket {bucket_name} is empty')
            table_files.add_row('*', '*', '*', '*', '*', '*')
            console.print(table_files)
            return

        for file in data:
            table_files.add_row(*file)
        console.print(table_files)

    def s3_bucket_create(self, bucket_name):
        self.s3_buckets.create_bucket(bucket_name)

    def s3_bucket_upload(self, bucket_name, file_path):
        # file_name = 'my_pdf_document.pdf'
        self.s3_buckets.upload_file(bucket_name, file_path)

