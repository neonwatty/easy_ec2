from easy_boto3.utilities.decorators import SessionAuthenticator
from easy_boto3.utilities.aws_profile_parser import get_aws_login_data
from easy_boto3 import active_profile_path
import yaml
import json


# create session authenticator based on aws credentials
def setup() -> SessionAuthenticator:
    # read in json file at active_profile_path
    with open(active_profile_path, 'r') as f:
        active_profile = json.load(f)

    # get profile name
    profile_name = active_profile['active_profile']

    # load in aws metadata
    aws_metadata = get_aws_login_data(profile_name)

    # create session authenticator
    session_auth = SessionAuthenticator(
        aws_access_key_id=aws_metadata['aws_access_key_id'],
        aws_secret_access_key=aws_metadata['aws_secret_access_key'],
        aws_region_name=aws_metadata['aws_profile_region'])

    return session_auth
