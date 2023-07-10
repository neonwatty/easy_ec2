import os
import sys
from easy_boto3.utilities.session_maker import SessionAuthenticator
from dotenv import dotenv_values

# add key directory to path
sys.path.insert(0, '/Users/wattjer/.ssh')

# path to this file
file_path = os.path.abspath(__file__)

# path to this file's directory
parent_directory = '/'.join(file_path.split('/')[:-1])

# path to parent of parent
parent_of_parent_directory = '/'.join(file_path.split('/')[:-2])

# path to base directory
base_directory = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))

# add to path
sys.path.append(parent_directory)
sys.path.append(base_directory)

# load in environment variables
config = dotenv_values(parent_of_parent_directory + "/.env")

# instantiate progress logger
session_auth = SessionAuthenticator(profile_name=config['profile_name'],
                                    region_name=config['region_name'])

# call out ids
aws_access_key_id = config['aws_access_key_id']
aws_secret_access_key = config['aws_secret_access_key']

# define path to scripts directory
scripts_path = os.path.join(parent_directory, 'scripts')
