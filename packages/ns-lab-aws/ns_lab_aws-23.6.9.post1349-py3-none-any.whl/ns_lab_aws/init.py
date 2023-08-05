import os
from ns_lab_aws.config.logging import logging_conf
from ns_lab_aws.config.environment import env_conf


user_path = os.getcwd()


# Search file logging.conf
file_logging = 'logging.conf'
path_logging = None

for root, dirs, files in os.walk(user_path):
    if file_logging in files:
        path_logging = os.path.join(root, file_logging)
        break

if path_logging is None:
    path_logging = f'{user_path}/{file_logging}'
    with open(path_logging, 'w') as logging_file:
        logging_file.write(logging_conf)


# Search file .env
file_env = '.env2'
path_env = None
for root, dirs, files in os.walk(user_path):
    if file_env in files:
        path_env = os.path.join(root, file_env)
        break

if path_env is None:
    path_env = f'{user_path}/{file_env}'
    with open(path_env, 'w') as dotenv_file:
        dotenv_file.write(env_conf)
