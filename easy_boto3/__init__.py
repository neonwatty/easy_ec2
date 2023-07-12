import os
import sys
from easy_boto3.utilities.decorators import SessionAuthenticator
from easy_boto3.utilities.aws_profile_parser import get_aws_metadata

### add paths ###
# path to this file
file_path = os.path.abspath(__file__)

# path to this file's directory
parent_directory = '/'.join(file_path.split('/')[:-1])

# path to base directory
base_directory = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))

# add to path
sys.path.append(parent_directory)
sys.path.append(base_directory)


### load in aws metadata ###
aws_metadata = get_aws_metadata()

### instance of decorators ###
session_auth = SessionAuthenticator(
    aws_access_key_id=aws_metadata['aws_access_key_id'],
    aws_secret_access_key=aws_metadata['aws_secret_access_key'],
    aws_profile_name=aws_metadata['aws_profile_name'],
    aws_region_name=aws_metadata['aws_profile_region'])
