from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def list_alarms(session=None):
    # create ec2 controller from session
    cloudwatch_client = session.client('cloudwatch')

    # List all alarms
    response = cloudwatch_client.describe_alarms()
    return response
