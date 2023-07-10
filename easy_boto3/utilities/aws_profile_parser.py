import os
import yaml
import configparser

file_path = os.path.abspath(__file__)
base_directory = '/'.join(file_path.split('/')[:-3])
easy_boto3_config_path = base_directory + '/.easy_boto3.yaml'


def get_easy_boto3_data() -> dict:
    # load in easy_boto3_config
    with open(easy_boto3_config_path, "r") as yaml_file:
        easy_boto3_config = yaml.safe_load(yaml_file)

    # unpack aws easy_boto3_config
    aws_data = easy_boto3_config["aws_data"]
    aws_config_directory = aws_data["aws_config_directory"]
    aws_profile_name = aws_data["profile_name"]
    aws_ssh_key = aws_data["aws_ssh_key"]

    # create dictionary
    easy_boto3_data = {
        "aws_config_directory": aws_config_directory,
        "aws_profile_name": aws_profile_name,
        "aws_ssh_key": aws_ssh_key
    }

    return easy_boto3_data


def get_aws_config_data(aws_config_path: str,
                        selected_profile_name: str) -> dict:
    # read in aws config
    aws_config = configparser.ConfigParser()
    aws_config.read(aws_config_path);

    # select data associated with selected profile
    aws_profile_region = aws_config[selected_profile_name]['region']
    aws_profile_output = aws_config[selected_profile_name]['output']

    return {'aws_profile_region': aws_profile_region, 'aws_profile_output': aws_profile_output}


def get_aws_creds_data(aws_creds_path: str,
                       selected_profile_name: str) -> dict:
    # read in credentials config
    aws_creds = configparser.ConfigParser()
    aws_creds.read(aws_creds_path);

    # select data associated with selected profile
    aws_access_key_id = aws_creds[selected_profile_name]['aws_access_key_id']
    aws_secret_access_key = aws_creds[selected_profile_name]['aws_secret_access_key']

    return {'aws_access_key_id': aws_access_key_id, 'aws_secret_access_key': aws_secret_access_key}


def get_aws_login_data(aws_config_directory: str,
                       selected_profile_name: str) -> dict:
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


def get_aws_metadata():
    ### load in config data ###
    # load in easy_boto3_config data
    easy_boto3_config = get_easy_boto3_data()

    # unpack aws easy_boto3_config
    aws_config_directory = easy_boto3_config["aws_config_directory"]
    aws_profile_name = easy_boto3_config["aws_profile_name"]
    aws_ssh_key = easy_boto3_config["aws_ssh_key"]

    # get aws login data
    aws_login_data = get_aws_login_data(aws_config_directory, aws_profile_name)

    # unpack aws login data
    aws_profile_region = aws_login_data["aws_profile_region"]
    aws_profile_output = aws_login_data["aws_profile_output"]
    aws_access_key_id = aws_login_data["aws_access_key_id"]
    aws_secret_access_key = aws_login_data["aws_secret_access_key"]

    # create object to store aws metadata
    aws_metadata = {
        "aws_profile_name": aws_profile_name,
        "aws_profile_region": aws_profile_region,
        "aws_profile_output": aws_profile_output,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "aws_ssh_key": aws_ssh_key
    }
    return aws_metadata
