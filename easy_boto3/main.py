

import sys
import yaml
import fire
from easy_boto3.ec2.config_parser import parse as ec2_config_parser
from easy_boto3.ec2.create import create_instance
from easy_boto3.ec2.stop import stop_instance
from easy_boto3.ec2.terminate import terminate_instance
from easy_boto3.ec2.list import list_all, list_running, list_stopped
from easy_boto3.cloudwatch.create import create_cpu_alarm
from easy_boto3.cloudwatch.list import list_alarms
from easy_boto3.cloudwatch.delete import delete_alarm


class EasyBoto3:
    def __init__(self):
        self.create_instance = create_instance
        self.stop_instance = stop_instance
        self.terminate_instance = terminate_instance
        self.list_all_instances = list_all
        self.list_stopped_instances = list_stopped
        self.list_running_instances = list_running

        self.create_cpu_alarm = create_cpu_alarm
        self.list_all_alarms = list_alarms
        self.delete_alarm = delete_alarm

    def ec2(self, sub_operation, **kwargs):
        if sub_operation == "create":
            return self.create_instance(**kwargs)
        elif sub_operation == "stop":
            return self.stop_instance(**kwargs)
        elif sub_operation == "terminate":
            return self.terminate_instance(**kwargs)
        elif sub_operation == "list_all":
            return self.list_all_instances(**kwargs)
        elif sub_operation == "list_stopped":
            return self.list_stopped_instances(**kwargs)
        elif sub_operation == "list_running":
            return self.list_running_instances(**kwargs)
        else:
            print("Invalid sub-operation for 'ec2'")

    def cloudwatch(self, sub_operation, **kwargs):
        if sub_operation == "create":
            return self.create_cpu_alarm(**kwargs)
        elif sub_operation == "list":
            return self.list_all_alarms(**kwargs)
        elif sub_operation == "delete":
            return self.delete_alarm(**kwargs)
        else:
            print("Invalid sub-operation for 'cloudwatch'")


if __name__ == "__main__":
    # create a dictionary from input args enumerating each command line argument given 
    # and its value
    args = dict(enumerate(sys.argv))

    # if there are four arguments, assume the final is config for now 
    if len(args) == 4:
        # if final argument contains '.yaml' assume it is config
        if args[2] == "create" and ".yaml" in args[3]:
            # get config path
            config = args[3]

            # ec2 config parser
            if args[1] == "ec2":
                ec2_instance_details = ec2_config_parser(config)
                launch_details = EasyBoto3().ec2("create", **ec2_instance_details)
                print(launch_details)
        if args[2] == "stop":
            if args[1] == "ec2":
                instance_id = args[3]
                stop_details = EasyBoto3().ec2("stop", instance_id=instance_id)
                print(stop_details)
        if args[2] == "terminate":
            if args[1] == "ec2":
                instance_id = args[3]
                terminate_details = EasyBoto3().ec2("terminate", instance_id=instance_id)
                print(terminate_details)
    elif len(args) == 3:
        if args[1] == "ec2":
            if 'list' in args[2]:
                instance_list = []
                if args[2] == "list_all":
                    instance_list = EasyBoto3().ec2(args[2])
                elif args[2] == "list_stopped":
                    instance_list = EasyBoto3().ec2(args[2])
                elif args[2] == "list_running":
                    instance_list = EasyBoto3().ec2(args[2])
                else:
                    print("Invalid sub-operation for 'ec2'")
                print(instance_list)





    # fire.Fire(EasyBoto3)
