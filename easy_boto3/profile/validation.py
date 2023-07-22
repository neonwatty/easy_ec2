import configparser
from easy_boto3 import aws_config_path, aws_creds_path


def validate(profile_name: str = 'default') -> None:
    # load in aws config file using configparser
    aws_config = configparser.ConfigParser()
    aws_config.read(aws_config_path)

    # check if profile name is valid
    if profile_name not in aws_config:
        raise ValueError('Profile name not found in aws config')


def check_credentials(profile_name: str = 'default') -> dict:
    # check if profile name is valid
    validate(profile_name)

    # load in aws config for read only using configparser
    aws_config = configparser.ConfigParser()
    aws_config.read(aws_creds_path)

    # retrieve profile secrets from aws_config
    profile_secrets = aws_config[profile_name]

    # transform into dictionary for return
    profile_secrets = dict(profile_secrets)
    return profile_secrets


def list_all_profiles() -> list:
    # load in aws config file using configparser
    aws_config = configparser.ConfigParser()
    aws_config.read(aws_config_path)

    # list of all profiles
    all_profile_sections = list(aws_config.sections())
    if len(all_profile_sections) == 0:
        print('No profiles found in aws config')
    else:
        # print profiles - one per line
        print('')
        print('all profiles found in aws config:')
        print('--------------------------------')
        for profile in all_profile_sections:
            print(profile)
        print('')
