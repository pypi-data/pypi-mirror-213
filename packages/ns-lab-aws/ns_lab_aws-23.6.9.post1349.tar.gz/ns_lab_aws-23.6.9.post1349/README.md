# Console for AWS

## How to use
 - Configure .env file
```
PYTHON_AWS_KEY=eEXAMPLEoIAN88J7LAH45X
PYTHON_AWS_SECRET=eEXAMPLEo2D4zGlMlwNrn7vC/rmKzxXz6X0cgj/
PYTHON_AWS_REGION=eu-central-1
```

- Install dependencies
```sh
pip install -r requirements.txt
```

- create file main.py
```python
from aws_admin import manager
```

- Run main.py

```sh
python -m main --help
```
```sh
(venv) salavat@Linux AWS % python -m ns_console.client --help
usage: client.py [-h] [--list] [--create] [--delete]
                 [--upload] [--download] [--content]
                 [--force] [-b BUCKET] [-f FILE] [-d DIR]

AWS S3 Buckets

options:
  -h, --help            show this help message and exit
  --list                List all buckets
  --create              Create bucket
  --delete              Delete bucket
  --upload              Upload file to bucket
  --download            Download file from bucket
  --content             Show bucket content
  --force               Force delete bucket
  -b BUCKET, --bucket BUCKET
                        Bucket name
  -f FILE, --file FILE  File name
  -d DIR, --dir DIR     Directory name
```
## Examples
### List all buckets
```sh
python -m main  --list
```
```sh
(venv) salavat@Linux AWS % python -m ns_console.client --list
                                                                                                            
                                               AWS S3 Buckets                                               
                                                                                                            
  ID   Files   Bucket                                                   Location             Created        
 ────────────────────────────────────────────────────────────────────────────────────────────────────────── 
  1        2   ns-lab.open-storage                                      EU-CENTRAL-1   2023-02-14 08:45:55  
  2        0   aws-sam-cli-managed-default-samclisourcebucket-1agj41…   EU-CENTRAL-1   2023-04-03 14:34:25  
  3        4   backname                                                 EU-CENTRAL-1   2023-06-07 13:32:36  
  4        0   2023-06-08-my-bucket                                     EU-CENTRAL-1   2023-06-08 06:02:00  
  5        2   new-storage4                                             EU-CENTRAL-1   2023-02-15 20:15:51  
  6       10   new-storage3                                             EU-CENTRAL-1   2023-02-15 14:00:37  
  7        1   zappa-s3-test1                                           EU-CENTRAL-1   2023-04-17 09:27:41  
  8      189   ns-lab-web                                               EU-WEST-3      2022-12-03 09:15:52 
```

### Create bucket
```sh
python -m main --create -b 'project-8.console'
```

### Delete bucket
```sh
python -m main --delete -b 'project-8.console'
```

### Show bucket content
```sh
python -m main  --content -b 'backname'  
```

```sh
                                                                                   
                              Files in AWS S3 Bucket                               
                                                                                   
   ID    Path   File                  Extension        Size         Created        
 ───────────────────────────────────────────────────────────────────────────────── 
   1            4100020573.pdf        PDF         350.64 KB   2023-06-07 19:34:09  
   2            Docker.dmg            DMG          590.5 MB   2023-06-07 19:35:26  
   3            flower.jpeg           JPEG        202.35 KB   2023-06-07 19:39:00  
   4            my_pdf_document.pdf   PDF         350.64 KB   2023-06-07 19:31:02  
```
