import os
from pathlib import Path

# path to user home directory
user_path = os.path.expanduser('~')

# path to aws config directory
aws_config_directory = user_path + '/.aws'
aws_config_path = aws_config_directory + '/config'
aws_creds_path = aws_config_directory + '/credentials'

# path to .easy_boto3 directory and internal config file
easy_boto3_directory = user_path + '/.easy_boto3'
internal_config_path = easy_boto3_directory + '/instance_profile_pairs.yaml'

# if internal yaml file does not exist, create it
if not Path(internal_config_path).exists():
    # create internal file
    Path(internal_config_path).touch()

    # add aws_profile: default to internal yaml file
    with open(internal_config_path, 'w') as f:
        f.write('aws_profile: default')
