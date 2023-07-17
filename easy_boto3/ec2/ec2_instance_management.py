from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def get_instance_public_ip(instance_id, session=None):
    # create ec2 controller from session
    ec2_controller = session.client('ec2')

    # get instance public ip
    response = ec2_controller.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['PublicIpAddress']


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
