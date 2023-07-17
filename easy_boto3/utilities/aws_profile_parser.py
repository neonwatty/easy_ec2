import configparser
from easy_boto3 import aws_config_directory


def get_aws_config_data(aws_config_path: str,
                        selected_profile_name: str) -> dict:
    # read in aws config
    aws_config = configparser.ConfigParser()
    aws_config.read(aws_config_path);

    # select data associated with selected profile
    aws_profile_region = aws_config[selected_profile_name]['region']
    aws_profile_output = aws_config[selected_profile_name]['output']

    return {'aws_profile_region': aws_profile_region,
            'aws_profile_output': aws_profile_output}


def get_aws_creds_data(aws_creds_path: str,
                       selected_profile_name: str) -> dict:
    # read in credentials config
    aws_creds = configparser.ConfigParser()
    aws_creds.read(aws_creds_path);

    # select data associated with selected profile
    aws_access_key_id = aws_creds[selected_profile_name]['aws_access_key_id']
    aws_secret_access_key = aws_creds[selected_profile_name]['aws_secret_access_key']

    return {'aws_access_key_id': aws_access_key_id,
            'aws_secret_access_key': aws_secret_access_key}


def get_aws_login_data(selected_profile_name: str) -> dict:
    # load in config from aws config directory
    aws_config_path = aws_config_directory + '/config'
    aws_creds_path = aws_config_directory + '/credentials'

    # get config data
    aws_config_data = get_aws_config_data(aws_config_path,
                                          selected_profile_name)

    # get creds data
    aws_creds_data = get_aws_creds_data(aws_creds_path, selected_profile_name)

    # merge all data
    all_aws_data = {}
    all_aws_data['profile_name'] = selected_profile_name
    all_aws_data.update(aws_config_data)
    all_aws_data.update(aws_creds_data)

    return all_aws_data
