from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def list_all(session=None):
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
def list_stopped(session=None):
    # get list of all instances
    all_instances = list_all()

    # collect stopped instances
    stopped_instances = []
    for instance in all_instances:
        # get instance data
        if instance['instance_state'] == 'stopped':
            stopped_instances.append(instance)

    return stopped_instances


@session_auth
def list_running(session=None):
    # get list of all instances
    all_instances = list_all()

    # collect running instances
    running_instances = []
    for instance in all_instances:
        # get instance data
        if instance['instance_state'] == 'running':
            running_instances.append(instance)

    return running_instances
