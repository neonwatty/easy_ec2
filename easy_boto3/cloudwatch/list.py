from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def list_alarms(session=None):
    # create cloudwatch controller from session
    cloudwatch_client = session.client('cloudwatch')

    # List all alarms
    response = cloudwatch_client.describe_alarms()
    return response


@session_auth
def list_instance_alarms(instance_id,
                         session=None):
    # create cloudwatch controller from session
    cloudwatch_client = session.client('cloudwatch')

    # List all alarms associated with instance_id
    response = cloudwatch_client.describe_alarms_for_metric(
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                },
            ]
        )
    return response
