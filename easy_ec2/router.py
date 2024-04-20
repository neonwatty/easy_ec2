from easy_ec2.compound import Compound


class Router(Compound):
    def __init__(self, cargs):
        self.args = dict(enumerate(cargs))

    def run(self):
        # process ec2 requests
        if self.args[1] == "ec2":
            if self.args[2] == "create" and ".yaml" in self.args[3]:
                config = self.args[3]
                create_report = self.create_ec2_instance(config)
                return create_report
            elif self.args[2] == "stop":
                instance_id = self.args[3]
                stop_report = self.stop_ec2_instance(instance_id)
                return stop_report
            elif self.args[2] == "terminate":
                instance_id = self.args[3]
                terminate_report = self.terminate_ec2_instance(instance_id)
                return terminate_report
            elif self.args[2] == "start":
                instance_id = self.args[3]
                start_report = self.start_ec2_instance(instance_id)
                return start_report
            elif self.args[2] == "check_cloud_init_logs":
                instance_id = self.args[3]
                self.check_cloud_init_logs(instance_id)
            elif self.args[2] == "check_syslog":
                instance_id = self.args[3]
                self.check_syslog(instance_id)
            elif self.args[2] == "list_all":
                instance_list = self.list_ec2_instances("list_all")
                return instance_list
            elif self.args[2] == "list_stopped":
                instance_list = self.list_ec2_instances("list_stopped")
                return instance_list
            elif self.args[2] == "list_running":
                instance_list = self.list_ec2_instances("list_running")
                return instance_list
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
