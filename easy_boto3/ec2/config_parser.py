import yaml
from easy_boto3.utilities.script_manager import read_startup_script 


def parse(base_config):
    # read in base_config
    with open(base_config, 'r') as stream:
        try:
            base_config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # parse config after first key 'instance_details'
    profile_name = base_config['aws_profile']
    ec2_instance_config = base_config['ec2_instance']
    instance_details = ec2_instance_config['instance_details']
    ssh_details = ec2_instance_config['ssh_details']
    script_details = ec2_instance_config['script_details']
    alarm_details = None
    alarm_instance_details = None

    # setup alarm_details if present in base_config
    if 'alarm_details' in list(base_config.keys()):
        alarm_details = base_config['alarm_details']
        alarm_instance_details = {}

        # parse alarm details
        alarm_instance_details['ComparisonOperator'] = alarm_details['ComparisonOperator']
        alarm_instance_details['EvaluationPeriods'] = alarm_details['EvaluationPeriods']
        alarm_instance_details['MetricName'] = alarm_details['MetricName']
        alarm_instance_details['Namespace'] = alarm_details['Namespace']
        alarm_instance_details['Period'] = alarm_details['Period']
        alarm_instance_details['Statistic'] = alarm_details['Statistic']
        alarm_instance_details['Threshold'] = alarm_details['Threshold']

    # read in startup script
    startup_script_filepath = script_details['filepath']
    UserData = read_startup_script(startup_script_filepath)

    # create dictionary of instance details
    ec2_instance_details = {
        'InstanceName': instance_details['InstanceName'],
        'InstanceType': instance_details['InstanceType'],
        'ImageId': instance_details['ImageId'],
        'Groups': instance_details['Groups'],
        'KeyName': ssh_details['KeyName'],
        'BlockDeviceMappings': [{
            'DeviceName': instance_details['BlockDeviceMappings']['DeviceName'],
            'Ebs': {
                'VolumeSize': instance_details['BlockDeviceMappings']['Ebs']['VolumeSize'],
                'VolumeType': instance_details['BlockDeviceMappings']['Ebs']['VolumeType'],
                'DeleteOnTermination': instance_details['BlockDeviceMappings']['Ebs']['DeleteOnTermination']
            }
          }],
        'UserData': UserData
    }

    # return dictionary of instance details
    return profile_name, ec2_instance_details, alarm_instance_details
