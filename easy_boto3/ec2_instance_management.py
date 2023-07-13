from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def launch_instance(key_name: str,
                    region='us-west-2',
                    instance_name='example_worker',
                    instance_type='t2.micro',
                    image_id='ami-03f65b8614a860c29',
                    tags=[{'Key': 'Name', 'Value': 'example_worker'}],
                    block_device_mappings=None,
                    security_group_ids=None,
                    startup_script: str = None,
                    session=None) -> object:

    # create ec2 controller from session
    ec2_controller = session.resource('ec2',
                                      region_name=region)
    # translate startup_script if None
    if startup_script is None:
        startup_script = '#!/bin/bash'

    # create a new EC2 instance
    instances = ec2_controller.create_instances(
        ImageId=image_id,
        NetworkInterfaces=[{
            'DeviceIndex': 0,
            'Groups': security_group_ids,
            'AssociatePublicIpAddress': True}],
        UserData=startup_script,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{'ResourceType': 'instance',
                            'Tags': tags}],
        InstanceType=instance_type,
        KeyName=key_name,
        Monitoring={'Enabled': True},
        BlockDeviceMappings=block_device_mappings,
        # enable IMDSv2
        MetadataOptions={
            'HttpTokens': 'required',
            'HttpEndpoint': 'enabled'
        }
     )

    # Wait for the instance to be running
    instances[0].wait_until_running()

    # Print the instance ID
    print("Instance created:", instances[0].id)

    return instances[0]


@session_auth
def get_instance_public_ip(instance_id, session=None):
    # create ec2 controller from session
    ec2_controller = session.client('ec2')

    # get instance public ip
    response = ec2_controller.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['PublicIpAddress']


@session_auth
def stop_instance(instance_id: str, 
                  session=None) -> str:
    # create ec2 controller from session
    ec2_controller = session.client('ec2')

    # check if instance is running
    response = ec2_controller.describe_instances(InstanceIds=[instance_id])
    if response['Reservations'][0]['Instances'][0]['State']['Name'] == 'running':
        # stop instance
        ec2_controller.stop_instances(InstanceIds=[instance_id])
        return f'instance {instance_id} stopped'
    else:
        return f'instance {instance_id} already stopped'


@session_auth
def terminate_instance(instance_id: str, 
                       session=None) -> str:
    # create ec2 controller from session
    ec2_controller = session.client('ec2')

    # Check if instance exists
    response = ec2_controller.describe_instances(InstanceIds=[instance_id])

    # Terminate instance if it exists
    if len(response["Reservations"]) > 0:
        # Terminate instance
        ec2_controller.terminate_instances(InstanceIds=[instance_id])
        return f"Instance {instance_id} terminated"
    else:
        return f"Instance {instance_id} does not exist"


@session_auth
def list_all_instances(session=None):
    # create ec2 controller from session
    ec2_controller = session.client('ec2')

    # List EC2 instances
    response = ec2_controller.describe_instances()

    # Extract instance information from the response
    instances = response['Reservations']
    all_instances = []
    for reservation in instances:
        for instance in reservation['Instances']:
            # get instance data
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            instance_type = instance['InstanceType']

            # package instance data in small dictionary 
            instance_data = {'instance_id': instance_id,
                             'instance_state': instance_state,
                             'instance_type': instance_type}

            # store instance information
            all_instances.append(instance_data)
    return all_instances


@session_auth
def list_stopped_instances(session=None):
    # get list of all instances
    all_instances = list_all_instances()

    # collect stopped instances
    stopped_instances = []
    for instance in all_instances:
        # get instance data
        if instance['instance_state'] == 'stopped':
            stopped_instances.append(instance)

    return stopped_instances


@session_auth
def list_running_instances(session=None):
    # get list of all instances
    all_instances = list_all_instances()

    # collect running instances
    running_instances = []
    for instance in all_instances:
        # get instance data
        if instance['instance_state'] == 'running':
            running_instances.append(instance)

    return running_instances


@session_auth
def terminate_all_stopped_instances(session=None):
    # get list of all stopped instances
    stopped_instances = list_stopped_instances()

    # create ec2 and cloudwatch controllers from session
    ec2_controller = session.client('ec2')
    cloudwatch_controller = session.client('cloudwatch')

    # List all stopped EC2 instances
    response = ec2_controller.describe_instances()

    # Extract instance information from the response
    stopped_instances = []
    instances = response['Reservations']
    for reservation in instances:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']

            # if instance state is stopped, add to list
            if instance_state == 'stopped':
                stopped_instances.append(instance_id)

    # terminate all stopped instances
    ec2_controller.terminate_instances(InstanceIds=stopped_instances)

    # terminate alarms for stopped instances
    cloudwatch_controller.delete_alarms(AlarmNames=stopped_instances)
