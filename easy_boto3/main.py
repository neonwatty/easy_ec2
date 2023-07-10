import os
from easy_boto3 import aws_metadata, session_auth

# path to this file and parent directory
file_path = os.path.abspath(__file__)
parent_directory = '/'.join(file_path.split('/')[:-1])


def main():
    pass
