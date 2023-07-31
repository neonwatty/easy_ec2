import sys
from easy_boto3.compound import Compound


class Router(Compound):
    def __init__(self):
        self.args = dict(enumerate(sys.argv))

    def run(self):
        # process ec2 requests
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
            elif self.args[2] == "start":
                instance_id = self.args[3]
                self.start_ec2_instance(instance_id)
            elif self.args[2] == "check_cloud_init_logs":
                instance_id = self.args[3]
                self.check_cloud_init_logs(instance_id)
            elif self.args[2] == "check_syslog":
                instance_id = self.args[3]
                self.check_syslog(instance_id)
            elif self.args[2] == "list_all":
                self.list_ec2_instances("list_all")
            elif self.args[2] == "list_stopped":
                self.list_ec2_instances("list_stopped")
            elif self.args[2] == "list_running":
                self.list_ec2_instances("list_running")
            else:
                print(f"Invalid sub-operation '{self.args[2]}' for 'ec2'")
        # process alarm requests
        elif self.args[1] == "alarm": 
            if self.args[2] == "list_all":
                self.list_all_alarms()
            elif self.args[2] == "list_instance":
                instance_id = self.args[3]
                self.list_alarm_instance(instance_id)
            else:
                print(f"Invalid sub-operation '{self.args[2]}' for 'alarm'")
        # process profile requests
        elif self.args[1] == "profile":
            if self.args[2] == "set":
                profile_name = self.args[3]
                self.profile("set", profile_name=profile_name)
            elif self.args[2] == "list_active":
                self.profile("list_active")
            elif self.args[2] == "list_all":
                self.profile("list_all")
            else:
                print(f"Invalid sub-operation '{self.args[2]}' for 'profile'")
        else:
            print(f"Invalid operation '{self.args[1]}'")
