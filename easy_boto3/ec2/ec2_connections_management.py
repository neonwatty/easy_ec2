import os, time
from easy_boto3 import session_auth
import paramiko
import logging
logging.getLogger("paramiko").setLevel(logging.CRITICAL)


def add_instance_to_known_hosts(instance_ip):
    # connect to instance
    username = 'ubuntu'
    key_path = '/Users/wattjer/.ssh/shiftsmart_transcript_west_2.pem'
    ec2_public_ip = instance_ip

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the EC2 instance
    ssh_client.connect(ec2_public_ip, username=username, key_filename=key_path)

    # loop over keys and add to known hosts lists
    all_keys = []
    all_names = set()
    client_key_types = paramiko.transport.Transport._preferred_keys
    for key_type in client_key_types:
        try:
            ssh_transport = paramiko.transport.Transport('%s:%s' % (instance_ip, 22))
            inner_options = ssh_transport.get_security_options()
            inner_options.key_types = (key_type,)

            ssh_transport.start_client()
            key = ssh_transport.get_remote_server_key()
            ssh_transport.close()

            name = key.get_name()
            if name not in all_names:
                all_names.add(name)
                all_keys.append(key)
        except:
            pass

    # Add the remote server's public keys to the local known_hosts file    
    home_dir = os.path.expanduser("~")
    known_hosts_path = os.path.join(home_dir, '.ssh', 'known_hosts')

    with open(known_hosts_path, 'a') as known_hosts_file:
        for key in all_keys:
            message = f'{instance_ip} {key.get_name()} {key.get_base64()}\n'
            known_hosts_file.write(message)

    # Close the SSH connection
    ssh_client.close()

    return True


def test_connect(instance_ip):
    username = 'ubuntu'
    key_path = '/Users/wattjer/.ssh/shiftsmart_transcript_west_2.pem'

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the EC2 instance
    ssh_client.connect(instance_ip, username=username, key_filename=key_path)


# try test_connect every 10 seconds 
def test_connection(instance_ip):
    max_count = 10
    while True:
        try:
            add_instance_to_known_hosts(instance_ip)
            print('addition to known hosts successful')
            break
        except:
            time.sleep(10)
            print('trying again')

        max_count -= 1
        if max_count == 0:
            print('max count reached')
            break
