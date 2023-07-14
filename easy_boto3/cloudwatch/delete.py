from easy_boto3.setup_session import setup
session_auth = setup()


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
