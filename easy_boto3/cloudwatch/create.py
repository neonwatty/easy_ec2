from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def create_cpu_alarm(instance_id,
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
