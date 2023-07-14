from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def launch_instance(KeyName: str,
                    InstanceName='example_worker',
                    InstanceType='t2.micro',
                    ImageId='ami-03f65b8614a860c29',
                    BlockDeviceMappings=None,
                    Groups=None,
                    UserData: str = None,
                    session=None) -> object:

    # create ec2 controller from session
    ec2_controller = session.resource('ec2')

    # translate startup_script if None
    if UserData is None:
        UserData = '#!/bin/bash'

    # create a new EC2 instance
    instances = ec2_controller.create_instances(
        ImageId=ImageId,
        NetworkInterfaces=[{
            'DeviceIndex': 0,
            'Groups': Groups,
            'AssociatePublicIpAddress': True}],
        UserData=UserData,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{'ResourceType': 'instance',
                            'Tags': [{'Key': 'Name',
                                      'Value': InstanceName}]}],
        InstanceType=InstanceType,
        KeyName=KeyName,
        Monitoring={'Enabled': True},
        BlockDeviceMappings=BlockDeviceMappings,
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
