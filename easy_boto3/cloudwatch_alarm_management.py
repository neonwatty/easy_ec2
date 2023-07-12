from easy_boto3 import session_auth


@session_auth
def setup_cpu_alarm(instance_id,
                    cpu_utilization_threshold=99.9,
                    session=None):
    # create ec2 controller from session
    ec2_client = session.client('ec2')
    cloudwatch_client = session.client('cloudwatch')

    # Enable detailed monitoring for the instance
    ec2_client.monitor_instances(InstanceIds=[instance_id])

    # Create a CloudWatch alarm for CPU usage
    alarm_name = 'cpu_alarm_' + instance_id

    # Create alarm
    result = cloudwatch_client.put_metric_alarm(
            AlarmName=alarm_name,
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            EvaluationPeriods=1,
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Period=60,
            Statistic='Average',
            Threshold=cpu_utilization_threshold,
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                },
            ],
        )

    return result


@session_auth
def list_all_alarms(session=None):
    # create ec2 controller from session
    cloudwatch_client = session.client('cloudwatch')

    # List all alarms
    response = cloudwatch_client.describe_alarms()

    return response


@session_auth 
def delete_alarm(alarm_name,
                 session=None):

    # create cloudwatch controller from session
    cloudwatch_client = session.client('cloudwatch')

    # delete alarm
    response = cloudwatch_client.delete_alarms(AlarmNames=[alarm_name])
    return response


@session_auth 
def delete_all_alarms(session=None):
    # create cloudwatch controller from session
    cloudwatch_client = session.client('cloudwatch')

    # list all alarms
    response = cloudwatch_client.describe_alarms()

    # delete all alarms
    alarm_delete_responses = []
    for alarm in response['MetricAlarms']:
        alarm_name = alarm['AlarmName']
        alarm_delete_response = cloudwatch_client.delete_alarms(AlarmNames=[alarm_name])
        alarm_delete_responses.append(alarm_delete_response)
    return alarm_delete_responses
