import os
from os.path import expanduser

# create paths
user_ssh_config = expanduser("~/.ssh/config")
easy_boto3_ssh_config = expanduser("~/.easy_boto3/ssh/config")
include_line = f'Include {easy_boto3_ssh_config}'

# create easy_boto3 directory at ~/.easy_boto3 if does not exist
if not os.path.exists(expanduser("~/.easy_boto3")):
    os.makedirs(expanduser("~/.easy_boto3"))

# create easy_boto3/ssh subdirectory at ~/.easy_boto3/ssh if does not exist
if not os.path.exists(expanduser("~/.easy_boto3/ssh")):
    os.makedirs(expanduser("~/.easy_boto3/ssh"))

# create config file in ~/.easy_boto3 if does not exist
if not os.path.exists(expanduser("~/.easy_boto3/ssh/config")):
    open(expanduser("~/.easy_boto3/ssh/config"), 'a').close()

# if include_line not in user_ssh_config then add at top of file
if include_line not in open(user_ssh_config).read():
    with open(user_ssh_config, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(include_line.rstrip('\r\n') + '\n' + content)
