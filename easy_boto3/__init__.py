import os

# path to aws config directory
aws_config_directory = os.path.expanduser('~') + '/.aws'
aws_config_path = aws_config_directory + '/config'

# construct path to internal yaml file
file_path = os.path.abspath(__file__)
library_path = os.path.dirname(file_path)

internal_config_path = library_path + '/.easy_boto3_internal.yaml'
