import os
from pathlib import Path

# path to aws config directory
aws_config_directory = os.path.expanduser('~') + '/.aws'
aws_config_path = aws_config_directory + '/config'
aws_creds_path = aws_config_directory + '/credentials'

# construct path to internal yaml file
file_path = os.path.abspath(__file__)
library_path = os.path.dirname(file_path)

# path to internal yaml file
internal_config_path = library_path + '/.easy_boto3_internal.yaml'

# if internal yaml file does not exist, create it
if not Path(internal_config_path).exists():
    # create internal file
    Path(internal_config_path).touch()

    # add aws_profile: default to internal yaml file
    with open(internal_config_path, 'w') as f:
        f.write('aws_profile: default')


