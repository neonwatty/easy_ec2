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
instance_id_profile_pairs_path = easy_boto3_directory + '/instance_id_profile_pairs.json'
active_profile_path = easy_boto3_directory + '/active_profile.json'

# if instance_id_profile_pairs_path does not exist, create it
if not Path(instance_id_profile_pairs_path).exists():
    # create file
    Path(instance_id_profile_pairs_path).touch()


# if active_profile_path does not exist, create it
if not Path(active_profile_path).exists():
    # create file
    Path(active_profile_path).touch()

    # write default profile object to file
    with open(active_profile_path, 'w') as file:
        file.write('{"active_profile": "default"}')
