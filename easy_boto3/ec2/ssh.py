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


@session_auth
def lookup_host_data_by_hostname(instance_ip,
                                 session=None):

    # get ssh config 
    config = create_config_object()

    # loop over hosts, find host with matching host_name = instance_ip
    for host in config.hosts():
        # lookup host_data config
        host_data = config.host(host)

        # lookup match for host_name = instance_ip
        if host_data['hostname'] == instance_ip:
            return host_data


@session_auth
def delete_host_by_hostname(instance_ip,
                            session=None):
    # get ssh config
    config = create_config_object()

    # loop over hosts, find host with matching host_name = instance_ip
    host_to_remove = None
    for host in config.hosts():
        # lookup host_data config
        host_data = config.host(host)

        # lookup match for host_name = instance_ip
        if host_data['hostname'] == instance_ip:
            host_to_remove = host
            break

    if host_to_remove is not None:
        config.remove(host_to_remove)
        config.save()

        print(f"Removing host with hostname '{instance_ip}' from ssh config")
    else:
        print(f"Host with hostname '{instance_ip}' NOT found in ssh config")
