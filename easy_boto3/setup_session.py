from easy_boto3.utilities.decorators import SessionAuthenticator
from easy_boto3.utilities.aws_profile_parser import get_aws_login_data
from easy_boto3 import internal_config_path
import yaml


# create session authenticator based on aws credentials
def setup() -> SessionAuthenticator:
    # load in internal config file for profile_name
    with open(internal_config_path, 'r') as f:
        internal_config = yaml.load(f, Loader=yaml.FullLoader)

    # get profile name
    profile_name = internal_config['aws_profile']

    # load in aws metadata
    aws_metadata = get_aws_login_data(profile_name)

    # create session authenticator
    session_auth = SessionAuthenticator(
        aws_access_key_id=aws_metadata['aws_access_key_id'],
        aws_secret_access_key=aws_metadata['aws_secret_access_key'],
        aws_region_name=aws_metadata['aws_profile_region'])

    return session_auth
