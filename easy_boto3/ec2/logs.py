import os
import paramiko
import logging
from easy_boto3.setup_session import setup
session_auth = setup()
logging.getLogger("paramiko").setLevel(logging.CRITICAL)


@session_auth
def check_cloud_init_logs(instance_ip,
                          ssh_username,
                          ssh_path_keypath,
                          session=None):
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the EC2 instance
    ssh_client.connect(instance_ip, username=ssh_username, key_filename=ssh_path_keypath)

    # Read and print the contents of the cloud-init output log file
    stdin, stdout, stderr = ssh_client.exec_command('cat /var/log/cloud-init-output.log')
    print(stdout.read().decode())

    # Close the SSH connection
    ssh_client.close()


@session_auth
def check_syslog(instance_ip,
                 ssh_username,
                 ssh_path_keypath,
                 session=None):
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the EC2 instance
    ssh_client.connect(instance_ip, username=ssh_username, key_filename=ssh_path_keypath)

    # Read and print the contents of the cloud-init output log file
    stdin, stdout, stderr = ssh_client.exec_command('cat /var/log/syslog')
    print(stdout.read().decode())

    # Close the SSH connection
    ssh_client.close()
