from easy_boto3 import session_auth


@session_auth
def launch_instance(script: str, 
                    session=None,
                    **kwargs) -> object:
    # create ec2 controller from session
    ec2_controller = session.resource('ec2', region_name='us-west-2')

    # optinally set config options
    InstanceName = 'transcript_worker'
    InstanceType = 't2.micro'
    ImageId = 'ami-03f65b8614a860c29'
    if 'InstanceName' in kwargs:
        InstanceName = kwargs['InstanceName']
    if 'InstanceType' in kwargs:
        InstanceType = kwargs['InstanceType']
    if 'ImageId' in kwargs:
        ImageId = kwargs['ImageId']

    # create a new EC2 instance
    instances = ec2_controller.create_instances(
        ImageId=ImageId,
        # IamInstanceProfile={'Arn': 'arn:aws:iam::829448320884:instance-profile/shiftsmart_ml'},
        NetworkInterfaces=[{
            'DeviceIndex': 0,
            'Groups': ['sg-0ad8c55f58167f63d'],
            'AssociatePublicIpAddress': True}],
        UserData=script,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{'ResourceType': 'instance',
                            'Tags': [{'Key': 'Name',
                                      'Value': InstanceName}]}],
        InstanceType=InstanceType,
        KeyName='shiftsmart_transcript_west_2',
        Monitoring={'Enabled': True},
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'VolumeSize': 300,
                    'VolumeType': 'gp2'
                }
            }
        ],
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
