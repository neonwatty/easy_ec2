from easy_ec2.ec2.config_parser import parse as ec2_config_parser
from easy_ec2.ec2.ssh import add_host
from easy_ec2.ec2.ssh import delete_host_by_hostname
from easy_ec2.ec2.ssh import lookup_host_data_by_hostname
from easy_ec2.ec2.ssh import delete_host
from easy_ec2.ec2.ssh import change_host_name_by_host
from easy_ec2.ec2.create import create_instance
from easy_ec2.ec2.stop import stop_instance
from easy_ec2.ec2.terminate import terminate_instance
from easy_ec2.ec2.start import start_instance
from easy_ec2.ec2.list import list_all as list_all_instances
from easy_ec2.ec2.list import list_running as list_running_instances
from easy_ec2.ec2.list import list_stopped as list_stopped_instances
from easy_ec2.ec2.logs import check_cloud_init_logs
from easy_ec2.ec2.logs import check_syslog
from easy_ec2.ec2.connect import get_public_ip


# centralized wiring chasis class for all current ec2 functionality
class EC2:
    def ec2(self, sub_operation, **kwargs):
        if sub_operation == "create":
            return create_instance(**kwargs)
        elif sub_operation == "stop":
            return stop_instance(**kwargs)
        elif sub_operation == "start":
            return start_instance(**kwargs)
        elif sub_operation == "terminate":
            return terminate_instance(**kwargs)
        elif sub_operation == "list_all":
            return list_all_instances(**kwargs)
        elif sub_operation == "list_stopped":
            return list_stopped_instances(**kwargs)
        elif sub_operation == "list_running":
            return list_running_instances(**kwargs)
        elif sub_operation == "check_cloud_init_logs":
            return check_cloud_init_logs(**kwargs)
        elif sub_operation == "check_syslog":
            return check_syslog(**kwargs)
        elif sub_operation == "get_public_ip":
            return get_public_ip(**kwargs)
        elif sub_operation == 'parse_config':
            return ec2_config_parser(**kwargs)
        else:
            print("Invalid sub-operation for 'ec2'")

    # chasis for ssh functionality
    def ssh(self, sub_operation, **kwargs):
        if sub_operation == "add":
            return add_host(**kwargs)
        elif sub_operation == 'delete_by_hostname':
            return delete_host_by_hostname(**kwargs)
        elif sub_operation == 'lookup_by_hostname':
            return lookup_host_data_by_hostname(**kwargs)
        elif sub_operation == 'delete':
            return delete_host(**kwargs)
        elif sub_operation == 'change_hostname':
            return change_host_name_by_host(**kwargs)
        else:
            print("Invalid sub-operation for 'ssh'")
