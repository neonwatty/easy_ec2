from easy_boto3.profile.active import set_active_profile
from easy_boto3.profile.active import list_active_profile
from easy_boto3.profile.validation import validate
from easy_boto3.profile.validation import list_all_profiles
from easy_boto3.profile.ownership import add_ownership_data
from easy_boto3.profile.ownership import delete_ownership_data
from easy_boto3.profile.ownership import change_ownership_state
from easy_boto3.profile.ownership import change_ownership_ip
from easy_boto3.ec2.config_parser import parse as ec2_config_parser
from easy_boto3.ec2.ssh import add_host
from easy_boto3.ec2.ssh import delete_host_by_hostname
from easy_boto3.ec2.ssh import lookup_host_data_by_hostname
from easy_boto3.ec2.ssh import delete_host
from easy_boto3.ec2.ssh import change_host_name_by_host
from easy_boto3.ec2.create import create_instance
from easy_boto3.ec2.stop import stop_instance
from easy_boto3.ec2.terminate import terminate_instance
from easy_boto3.ec2.start import start_instance
from easy_boto3.ec2.list import list_all as list_all_instances
from easy_boto3.ec2.list import list_running as list_running_instances
from easy_boto3.ec2.list import list_stopped as list_stopped_instances
from easy_boto3.ec2.logs import check_cloud_init_logs
from easy_boto3.ec2.logs import check_syslog
from easy_boto3.cloudwatch.create import create_cpu_alarm
from easy_boto3.cloudwatch.list import list_alarms
from easy_boto3.cloudwatch.list import list_instance_alarms
from easy_boto3.cloudwatch.delete import delete_alarm
from easy_boto3.ec2.connect import get_public_ip
from easy_boto3.ec2.ssh import add_host
from easy_boto3.ec2.ssh import delete_host_by_hostname
from easy_boto3.ec2.ssh import lookup_host_data_by_hostname
from easy_boto3.ec2.ssh import delete_host
from easy_boto3.ec2.ssh import change_host_name_by_host


# centralized wiring chasis class for all current functionality
class Base:
    # chasis for profile functionality
    def profile(self, sub_operation, **kwargs):
        if sub_operation == "add":
            return add_ownership_data(**kwargs)
        if sub_operation == "delete":
            return delete_ownership_data(**kwargs)
        if sub_operation == "change_state":
            return change_ownership_state(**kwargs)
        if sub_operation == "change_ip":
            return change_ownership_ip(**kwargs)
        if sub_operation == "validate":
            return validate(**kwargs)
        if sub_operation == "list_all":
            return list_all_profiles(**kwargs)
        if sub_operation == "set":
            return set_active_profile(**kwargs)
        if sub_operation == "list_active":
            return list_active_profile(**kwargs)

    # chasis for ec2 functionality
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

    # chasis for all cloudwatch functionality
    def cloudwatch(self, sub_operation, **kwargs):
        if sub_operation == "create":
            return create_cpu_alarm(**kwargs)
        elif sub_operation == "list_all":
            return list_alarms(**kwargs)
        elif sub_operation == "list_instance":
            return list_instance_alarms(**kwargs)
        elif sub_operation == "delete":
            return delete_alarm(**kwargs)
        else:
            print("Invalid sub-operation for 'cloudwatch'")
 
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
