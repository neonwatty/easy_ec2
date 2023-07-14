import yaml
from easy_boto3.utilities.script_manager import read_startup_script 


def parse(config):
    # read in config 
    with open(config, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # parse config after first key 'instance_details'
    ec2_instance_config = config['ec2_instance']
    instance_details = ec2_instance_config['instance_details']
    ssh_details = ec2_instance_config['ssh_details']
    script_details = ec2_instance_config['script_details']

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
    return ec2_instance_details
