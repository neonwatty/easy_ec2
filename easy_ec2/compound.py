from easy_ec2.ec2.ec2 import EC2
from easy_ec2.profile.profile import Profile
from easy_ec2.cloudwatch.cloudwatch import Cloudwatch


class Compound(EC2, Profile, Cloudwatch):
    def create_ec2_instance(self, config):
        # readin config file
        profile_name, ec2_instance_details, alarm_instance_details, ssh_instance_details = \
            self.ec2("parse_config",
                     base_config=config)

        # set aws profile name
        self.profile("validate",
                     profile_name=profile_name)

        # create ec2 instance
        launch_details = self.ec2("create", **ec2_instance_details)

        # record instance_id / profile pair in ~/.easy_ec2/instance_profile_pairs.yaml
        self.profile("add",
                     instance_id=launch_details.id,
                     public_ip=launch_details.public_ip,
                     profile_name=profile_name)

        # unpack ssh_details
        ssh_config_settings = ssh_instance_details['Config']
        # ssh_options = ssh_instance_details['Options']

        # set host if present in config
        host = None
        if 'Host' in list(ssh_config_settings.keys()):
            host = ssh_config_settings['Host']
            del ssh_config_settings['Host']

        else:  # by default, set host to instance_id
            host = launch_details.id

        # package host_info - remove Host key and add public_ip
        ssh_config_settings['HostName'] = launch_details.public_ip

        # add host to ssh config
        self.ssh('add',
                 host=host,
                 host_info=ssh_config_settings)

        # set alarm if present in config
        if alarm_instance_details is not None:
            alarm_instance_details['instance_id'] = launch_details.id
            alarm_details = self.cloudwatch("create", **alarm_instance_details)
            print(f"Alarm created - alarm_name = {alarm_details['AlarmName']}")
        else:
            print("No alarm created")

        # return launch details report
        report = {'instance_id': launch_details.id, 'instance_state': 'running', 'public_ip' : launch_details.public_ip}
        return report

    def stop_ec2_instance(self, instance_id):
        # lookup public_ip associated with instance_id
        instance_ip = self.ec2('get_public_ip',
                               instance_id=instance_id)

        # stop instance
        self.ec2('stop',
                 instance_id=instance_id)

        # adjust instance state in file
        self.profile("change_state",
                     instance_id=instance_id,
                     new_state="stopped")

        # return report updated instance_ip
        report = {'instance_id': instance_id, 'instance_state': 'stopped', 'public_ip' : instance_ip}
        return report

    def terminate_ec2_instance(self, instance_id):
        # lookup public_ip associated with instance_id
        instance_ip = self.ec2('get_public_ip',
                               instance_id=instance_id)

        # delete instance and alarm associated with instance_id
        terminate_details = self.ec2("terminate", instance_id=instance_id)
        if terminate_details is not None:
            pass

        # delete entry in ~/.easy_ec2/ssh_config associated with HostName = instance_ip
        self.ssh('delete',
                 host=instance_id)

        # delete profile pair entry
        self.profile("delete", instance_id=instance_id)

        # print updated instance_ip
        report = {'instance_id': instance_id, 'instance_state': 'terinated', 'public_ip' : instance_ip}
        return report

    def start_ec2_instance(self, instance_id):
        # start instance
        self.ec2('start',
                 instance_id=instance_id)

        # lookup public_ip associated with instance_id
        instance_ip = self.ec2('get_public_ip',
                               instance_id=instance_id)

        # adjust instance state in file
        self.profile("change_state",
                     instance_id=instance_id,
                     new_state="running")

        # adjust public_ip in pair file
        self.profile("change_ip",
                     instance_id=instance_id,
                     public_ip=instance_ip)

        # change host name in ssh config
        self.ssh('change_hostname',
                 host=instance_id,
                 public_ip=instance_ip)

        # updated instance_ip
        report = {'instance_id': instance_id, 'instance_state': 'running', 'public_ip' : instance_ip}
        return report

    def list_ec2_instances(self, sub_operation):
        instance_list = []
        if sub_operation == "list_all":
            instance_list = self.ec2(sub_operation)
            return instance_list
        elif sub_operation == "list_stopped":
            instance_list = self.ec2(sub_operation)
            return instance_list
        elif sub_operation == "list_running":
            instance_list = self.ec2(sub_operation)
            return instance_list
        else:
            print("Invalid sub-operation for 'ec2'")
        for item in instance_list:
            print(item)

    def check_cloud_init_logs(self, instance_id):
        # lookup public_ip associated with instance_id
        instance_ip = self.ec2('get_public_ip',
                               instance_id=instance_id)

        # lookup host_data by instance_ip
        host_data = self.ssh('lookup_by_hostname',
                             instance_id=instance_ip)

        # read logs if host_data is not none
        if host_data is not None:
            ssh_username = host_data['user']
            ssh_path_keypath = host_data['identityfile']
            self.ec2("check_cloud_init_logs",
                     instance_ip=instance_ip,
                     ssh_username=ssh_username,
                     ssh_path_keypath=ssh_path_keypath)

    def check_syslog(self, instance_id):
        # lookup public_ip associated with instance_id
        instance_ip = self.ec2('get_public_ip',
                               instance_id=instance_id)

        # use public_ip to lookup ssh_config_settings
        host_data = self.ssh('lookup_by_hostname',
                             instance_ip=instance_ip)

        # read logs if host_data is not none
        if host_data is not None:
            ssh_username = host_data['user']
            ssh_path_keypath = host_data['identityfile']
            self.ec2("check_syslog",
                     instance_ip=instance_ip,
                     ssh_username=ssh_username,
                     ssh_path_keypath=ssh_path_keypath)

    def list_alarm_instance(self, instance_id):
        alarm_list = self.cloudwatch("list_instance", instance_id=instance_id)
        for item in alarm_list:
            print(item)

    def list_all_alarms(self):
        alarm_list = self.cloudwatch("list_all")
        for item in alarm_list:
            print(item)
