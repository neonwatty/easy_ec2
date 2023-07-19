from sshconf import read_ssh_config
from os.path import expanduser
from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def create_config_object(session=None):
    config = read_ssh_config(expanduser("~/.easy_boto3/ssh/config"))
    return config


@session_auth
def read_raw_config(session=None):
    # read current list of hosts from ssh config
    config = create_config_object()
    print(config.config())


@session_auth
def read_hosts(session=None):
    # read current list of hosts from ssh config
    config = create_config_object()
    return config.hosts()


@session_auth
def add_host(host,
             host_info,
             session=None):
    # add host to ssh config
    config = create_config_object()

    # check if host already exists in ssh config
    if host in config.hosts():
        print(f"Host '{host}' already exists in ssh config")
        return

    # otherwise add host to ssh config
    config.add(host, **host_info)
    config.save()


@session_auth
def delete_host(host,
                session=None):
    # delete host from ssh config
    config = create_config_object()
    config.remove(host)
    config.save()
