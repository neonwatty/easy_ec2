from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def create_cpu_alarm(instance_id=None,
                     ComparisonOperator='GreaterThanOrEqualToThreshold',
                     EvaluationPeriods=10,
                     MetricName='CPUUtilization',
                     Namespace='AWS/EC2',
                     Period=60,
                     Statistic='Average',
                     Threshold=99.9,
                     session=None):
    # create ec2 controller from session
    ec2_client = session.client('ec2')
    cloudwatch_client = session.client('cloudwatch')

    # create instance_id stamped alarm name
    AlarmName = '{}-{}'.format('cpu_alarm', instance_id)

    # construct simple dimension
    Dimensions = [{
            'Name': 'InstanceId',
            'Value': instance_id
        }]

    # Enable detailed monitoring for the instance
    ec2_client.monitor_instances(InstanceIds=[instance_id])

    # Create alarm
    result = cloudwatch_client.put_metric_alarm(
            AlarmName=AlarmName,
            ComparisonOperator=ComparisonOperator,
            EvaluationPeriods=EvaluationPeriods,
            MetricName=MetricName,
            Namespace=Namespace,
            Period=Period,
            Statistic=Statistic,
            Threshold=Threshold,
            Dimensions=Dimensions
        )

    return {'AlarmName': AlarmName}
