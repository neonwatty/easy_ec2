import sys
from easy_boto3.profile import profile
from easy_boto3.ec2.config_parser import parse as ec2_config_parser
from easy_boto3.ec2.ssh import add_host
from easy_boto3.ec2.create import create_instance
from easy_boto3.ec2.stop import stop_instance
from easy_boto3.ec2.terminate import terminate_instance
from easy_boto3.ec2.list import list_all, list_running, list_stopped
from easy_boto3.ec2.logs import check_cloud_init_logs
from easy_boto3.cloudwatch.create import create_cpu_alarm
from easy_boto3.cloudwatch.list import list_alarms, list_instance_alarms
from easy_boto3.cloudwatch.delete import delete_alarm


class EasyBoto3:
    def __init__(self):
        self.create_instance = create_instance
        self.stop_instance = stop_instance
        self.terminate_instance = terminate_instance
        self.list_all_instances = list_all
        self.list_stopped_instances = list_stopped
        self.list_running_instances = list_running
        self.check_cloud_init_logs = check_cloud_init_logs

        self.create_cpu_alarm = create_cpu_alarm
        self.list_all_alarms = list_alarms
        self.list_instance_alarms = list_instance_alarms
        self.delete_alarm = delete_alarm

    def profile(self, sub_operation, **kwargs):
        if sub_operation == "set":
            return profile.set(**kwargs)
        if sub_operation == "check":
            return profile.check(**kwargs)
        if sub_operation == "validate":
            return profile.validate(**kwargs)

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
        elif sub_operation == "check_cloud_init_logs":
            return self.check_cloud_init_logs(**kwargs)
        else:
            print("Invalid sub-operation for 'ec2'")

    def cloudwatch(self, sub_operation, **kwargs):
        if sub_operation == "create":
            return self.create_cpu_alarm(**kwargs)
        elif sub_operation == "list_all":
            return self.list_all_alarms(**kwargs)
        elif sub_operation == "list_instance":
            return self.list_instance_alarms(**kwargs)
        elif sub_operation == "delete":
            return self.delete_alarm(**kwargs)
        else:
            print("Invalid sub-operation for 'cloudwatch'")


class Application:
    def __init__(self):
        self.args = dict(enumerate(sys.argv))
        self.easy_boto3 = EasyBoto3()

    def run(self):
        if len(self.args) == 4:
            self.process_four_arguments()
        elif len(self.args) == 3:
            self.process_three_arguments()

    def process_four_arguments(self):
        if self.args[1] == "ec2":
            if self.args[2] == "create" and ".yaml" in self.args[3]:
                config = self.args[3]
                self.create_ec2_instance(config)
            elif self.args[2] == "stop":
                instance_id = self.args[3]
                self.stop_ec2_instance(instance_id)
            elif self.args[2] == "terminate":
                instance_id = self.args[3]
                self.terminate_ec2_instance(instance_id)
            elif self.args[2] == "check_cloud_init_logs":
                instance_id = self.args[3]
                self.check_cloud_init_logs(instance_id)    
        elif self.args[1] == 'alarm':
            if self.args[2] == 'list_instance':
                instance_id = self.args[3]
                self.list_alarm_instance(instance_id)
            else:
                print(f"Invalid sub-operation '{self.args[2]}' for 'alarm'")
        else:
            print(f"Invalid operation / sub-operation '{self.args}'")

    def process_three_arguments(self):
        if self.args[1] == "ec2":
            if 'list' in self.args[2]:
                self.list_ec2_instances(self.args[2])
            else:
                print(f"Invalid sub-operation '{self.args[2]}' for 'ec2'")
        elif self.args[1] == 'alarm':
            if self.args[2] == 'list_all':
                self.list_all_alarms()
            else:
                print(f"Invalid sub-operation '{self.args[2]}' for 'alarm'")

    def create_ec2_instance(self, config):
        # readin config file
        profile_name, ec2_instance_details, alarm_instance_details, ssh_instance_details = ec2_config_parser(config)

        # set aws profile name
        self.easy_boto3.profile("set", profile_name=profile_name)

        # create ec2 instance
        launch_details = self.easy_boto3.ec2("create", **ec2_instance_details)
        print(f"Instance created - instance_id = {launch_details.id} and public_ip = {launch_details.public_ip}")

        # unpack ssh_details
        ssh_config_settings = ssh_instance_details['Config']
        ssh_options = ssh_instance_details['Options']

        # set host if present in config
        if 'Host' in list(ssh_config_settings.keys()):
            host = ssh_config_settings['Host']

            # package host_info - remove Host key and add public_ip
            del ssh_config_settings['Host']
            ssh_config_settings['HostName'] = launch_details.public_ip
            print(ssh_config_settings)

            # add host to ssh config
            add_host(host, ssh_config_settings)

        # set alarm if present in config
        if alarm_instance_details is not None:
            alarm_instance_details['instance_id'] = launch_details.id
            alarm_details = self.easy_boto3.cloudwatch("create", **alarm_instance_details)
            print(f"Alarm created - alarm_name = {alarm_details['AlarmName']}")

    def check_cloud_init_logs(self, instance_id):
        instance_ip = self.easy_boto3.ec2("list_running", instance_id=instance_id)
        self.easy_boto3.ec2("check_cloud_init_logs", instance_ip=instance_ip, config=config)

    def list_ec2_instances(self, sub_operation):
        instance_list = []
        if sub_operation == "list_all":
            instance_list = self.easy_boto3.ec2(sub_operation)
        elif sub_operation == "list_stopped":
            instance_list = self.easy_boto3.ec2(sub_operation)
        elif sub_operation == "list_running":
            instance_list = self.easy_boto3.ec2(sub_operation)
        else:
            print("Invalid sub-operation for 'ec2'")
        for item in instance_list:
            print(item)

    def list_alarm_instance(self, instance_id):
        alarm_list = self.easy_boto3.cloudwatch("list_instance", instance_id=instance_id)
        for item in alarm_list:
            print(item)

    def stop_ec2_instance(self, instance_id):
        stop_details = self.easy_boto3.ec2("stop", instance_id=instance_id)

    def terminate_ec2_instance(self, instance_id):
        terminate_details = self.easy_boto3.ec2("terminate", instance_id=instance_id)

    def list_all_alarms(self):
        alarm_list = self.easy_boto3.cloudwatch("list_all")
        for item in alarm_list:
            print(item)

    def ec2_cloud_init_logs(self, instance_ip, config):
        profile_name, ec2_instance_details, alarm_instance_details = ec2_config_parser(config)
        self.check_cloud_init_logs(instance_ip, ec2_instance_details['UserName'], ec2_instance_details['KeyName'])


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()