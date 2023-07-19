from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def read_ssh_config(file_path):
    hosts = {}
    current_host = None

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('Host '):
                host_name = line.split(' ')[1]
                hosts[host_name] = {}
                current_host = host_name
            elif line.startswith('HostName '):
                hosts[current_host]['HostName'] = line.split(' ')[1]
            elif line.startswith('User '):
                hosts[current_host]['User'] = line.split(' ')[1]
            elif line.startswith('ForwardAgent '):
                hosts[current_host]['ForwardAgent'] = line.split(' ')[1]
            elif line.startswith('IdentityFile '):
                hosts[current_host]['IdentityFile'] = line.split(' ')[1]

    return hosts


@session_auth
def delete_host(file_path, host_name):
    config_lines = []

    with open(file_path, 'r') as f:
        config_lines = f.readlines()

    with open(file_path, 'w') as f:
        for line in config_lines:
            if not line.startswith('Host ' + host_name):
                f.write(line)


@session_auth
def add_host(file_path, host_name, host_info):
    with open(file_path, 'a') as f:
        f.write(f'\nHost {host_name}\n')
        for key, value in host_info.items():
            f.write(f'    {key} {value}\n')
