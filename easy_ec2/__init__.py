import os
from pathlib import Path

# path to lib
library_base_dir = os.path.dirname(os.path.abspath(__file__))

# parent of library_base_dir
library_root_dir = os.path.dirname(library_base_dir)

# path to user home directory
user_path = os.path.expanduser('~')

# path to aws config directory
aws_config_directory = user_path + '/.aws'
aws_config_path = aws_config_directory + '/config'
aws_creds_path = aws_config_directory + '/credentials'

# path to .easy_ec2 directory
easy_ec2_directory = user_path + '/.easy_ec2'

# if easy_ec2_directory does not exist, create it
if not Path(easy_ec2_directory).exists():
    # create directory
    os.mkdir(easy_ec2_directory)

    # create ssh subdirectory
    os.mkdir(easy_ec2_directory + '/ssh')

# if /user_path/.ssh does not exist, create it
if not Path(user_path + '/.ssh').exists():
    # create directory
    os.mkdir(user_path + '/.ssh')

# if /user_path/.ssh/config does not exist, create it
if not Path(user_path + '/.ssh/config').exists():
    # create file
    Path(user_path + '/.ssh/config').touch()

    # write Include easy_ec2_directory + '/ssh/config' in ~/.ssh/config
    with open(user_path + '/.ssh/config', 'w') as file:
        file.write(f'Include {easy_ec2_directory}/ssh/config')

# paths to internal config files based off easy_ec2_directory
instance_id_profile_pairs_path = easy_ec2_directory + '/instance_id_profile_pairs.json'
active_profile_path = easy_ec2_directory + '/active_profile.json'

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
