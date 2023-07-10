from easy_boto3 import session_auth


@session_auth
def list_all_instancess(session=None):
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
    all_instances = list_all_instancess()

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
    all_instances = list_all_instancess()

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
