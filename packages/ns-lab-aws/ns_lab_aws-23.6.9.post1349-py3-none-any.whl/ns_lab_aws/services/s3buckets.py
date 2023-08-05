from ns_lab_aws.converter.converter import convert_bytes
from ns_lab_aws.config.settings import aws_session, aws_region
from ns_lab_aws.config.settings import logger
from ns_lab_aws.config.libraries import List, Union, Dict, Any
from ns_lab_aws.config.libraries import print
from ns_lab_aws.config.libraries import threading, os 


logger = logger.getLogger('NS_AWS:S3Buckets')


class S3Buckets:
    '''Class for AWS S3 buckets'''
    def __init__(self):
        self.s3_client = aws_session.client('s3')

    def list_buckets(self) -> Union[List, False]:
        '''List all buckets in S3'''

        # Part 0: Prepare variables and constants
        log_header       = 'List Buckets:'
        self.bucket_list = []
        thread_list      = []

        # Part 1: Get all buckets
        aws_s3_buckets = self.s3_client.list_buckets()
        status_code    = aws_s3_buckets['ResponseMetadata']['HTTPStatusCode']
        all_buckets    = aws_s3_buckets['Buckets']

        # Part 2: Check-1: Status code
        if status_code != 200:
            logger.error(f'{log_header} status_code is {status_code};')
            return False

        # Part 3: Start threads for each bucket
        for bucket in all_buckets:
            thread = threading.Thread(target=self.process_bucket, args=(bucket,))
            thread.start()
            thread_list.append(thread)
 
        # Part 4: Wait for all threads
        for thread in thread_list:
            thread.join()

        return self.bucket_list
    
    def process_bucket(self, bucket) -> None:
        '''Process for each bucket'''

        # Part 0: Prepare variables and constants
        log_header    = 'ProcessBucket:'      
        bucket_name   = bucket['Name'] 
        count_content = self.process_count_files(bucket_name)
        created_date  = bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')
        bucket_region = self.process_bucket_region(bucket_name)

        # Part 1: Prepare data for bucket
        bucket_dict = {
            'bucket':   str(bucket_name),
            'created':  str(created_date),
            'location': str(bucket_region).upper(),
            'content':  str(count_content)
        }
        self.bucket_list.append(bucket_dict)

    def create_bucket(self, bucket_name):
        '''Create bucket'''

        log_header = 'Creating:'

        # Part-1: Check-1: If bucket_name is None, return False
        if bucket_name is None:
            logger.error(f'{log_header} bucket_name is None;')
            logger.warning(f'{log_header} Please provide bucket_name. Use -b "bucket-name" option.')
            return False
        
        # Part-2: Prepare data - bucket_name and region
        data = {
            'Bucket': bucket_name,
            'CreateBucketConfiguration': {
                'LocationConstraint': aws_region
                }
            }
        
        # Part-3: Create bucket
        try:
            response = self.s3_client.create_bucket(**data)
        except Exception as error:
            msg_err = str(error)
            # print(msg_err)
            if '(BucketAlreadyOwnedByYou)'in msg_err:
                logger.info(f'{log_header} Bucket "{bucket_name}" already exists;')
                return True
            elif '(InvalidBucketName)' in msg_err:
                logger.error(f'{log_header} Bucket name "{bucket_name}" is not valid;')
                logger.warning(f'{log_header} Allowed characters are a-z, ".", "-", 0-9;')
                return False

            msg = str(error.response['Error']['Message'])
            logger.error(f'{log_header} {msg}')

            return False
        
        status_code = response['ResponseMetadata']['HTTPStatusCode']

        # Part-4: Check-2: If status_code is not 200, return False
        if status_code != 200:
            logger.error(f'{log_header} status_code is {status_code};')
            return False
        
        # Part-5: Check-3: If status_code is 200, return True
        
        logger.info(f'{log_header} Bucket "{bucket_name}" created;')
        return True

    def delete_bucket(self, bucket_name, force):
        '''Delete bucket'''
        log_header = 'Delete:'

       
        if force:
            try:
                full_objects = self.s3_client.list_objects_v2(Bucket=bucket_name)['Contents']
                full_version = self.s3_client.list_object_versions(Bucket=bucket_name)['Versions'] # CHECK here aws-sam-cli-managed-default-samclisourcebucket-1agj41omw8jre
                list_objects = [{'Key': obj['Key']} for obj in full_objects]
                print(list_objects)
                self.s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': list_objects})
            except Exception as error:
                msg = error.response['Error']['Message']
                logger.error(f'{log_header} {msg}')
                return False
                
        try:
            self.s3_client.delete_bucket(Bucket=bucket_name)
        except Exception as error:
            msg = error.response['Error']['Message']
            logger.error(f'{log_header} {msg}')
            if "(BucketNotEmpty)" in str(error):
                logger.warning(f'{log_header} for check contents of bucket, use --content option;')
                logger.warning(f'{log_header} for delete bucket forcefully, use --force   option;')
            return False
        
        return True
        
        
        

    def content_bucket(self, bucket_name):
        '''Content bucket'''

        # Part 0: Prepare variables and constants
        log_header = 'ContentBucket:'
        thread_list = []

        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
        except Exception as error:
            msg = error.response['Error']['Message']
            logger.error(f'{log_header} {msg}')
            return False
        
        
        bucket_content  = response['Contents']
        self.list_files = []

        count_of_files = len(bucket_content)
        print(f' - Count of files: {count_of_files}')



        # file_count = 0

        # for filepath in bucket_content:
        #     thread = threading.Thread(target=self.process_path, args=(filepath,))
        #     thread.start()
        #     thread_list.append(thread)
 
        # for thread in thread_list:
        #     thread.join()
     
        file_count = 0
        for filepath in bucket_content:
            
            full_file_path = filepath['Key']
            
            # Part-1: Skip if folder is hidden (.git, .vscode, etc.)
            if '/.' in full_file_path:
                continue
            
            # Part-2: Get File name and Full Path
            file_count += 1
            file_name   = full_file_path.split('/')[-1]
            file_path   = full_file_path.replace(file_name, '')
            extension   = file_name.split('.')[-1].upper()
            created     = filepath['LastModified'].strftime("%Y-%m-%d %H:%M:%S")
            file_size   = filepath['Size']
            size, unit  = convert_bytes(file_size)
            file_size   = f'{size} {unit}'
            file_option = [str(file_count), file_path, file_name, extension, file_size, created]
            self.list_files.append(file_option)

        return self.list_files

    def process_count_files(self, bucket_name):
        try:
            bucket_objects  = self.s3_client.list_objects_v2(Bucket=bucket_name)
            count_content   = len(bucket_objects['Contents'])
        except Exception as error:
            count_content = 0
        return count_content

    def process_bucket_region(self, bucket_name):
        try:
            response      = self.s3_client.get_bucket_location(Bucket=bucket_name)
            bucket_region = response['LocationConstraint']
            if bucket_region is None:
                bucket_region = 'us-east-1'
        except Exception as error:
            bucket_region = '-- Not found --'

        return bucket_region

    def upload_file(self, bucket_name, file_path):
        '''Upload file'''
        log_header = 'UploadFile:'

        file_name = file_path.split('/')[-1]

        # Part-3: Check-3: If bucket_name is None, return False
        if bucket_name is None:
            logger.error(f'{log_header} bucket_name is None;')
            logger.warning(f'{log_header} Please provide bucket_name. Use -b "bucket-name" option.')
            return False

        # Part-4: Check-4: If file_path is not valid, return False
        if not os.path.exists(file_path):
            logger.error(f'{log_header} file_path "{file_path}" is not valid;')
            return False


        # Part-7: Upload file
        try:
            self.s3_client.upload_file(file_path, bucket_name, file_name)
        except Exception as error:
            msg = error.response['Error']['Message']
            logger.error(f'{log_header} {msg}')
            return False

        logger.info(f'{log_header} File "{file_name}" uploaded successfully.')
        return True
