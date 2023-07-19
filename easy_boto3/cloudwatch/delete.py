from easy_boto3.setup_session import setup
session_auth = setup()
from easy_boto3.cloudwatch.list import list_instance_alarms


@session_auth
def delete_alarm(AlarmName: str,
                 session=None):

    # create cloudwatch controller from session
    cloudwatch_client = session.client('cloudwatch')

    # delete alarm
    response = cloudwatch_client.delete_alarms(AlarmNames=[AlarmName])
    return response


@session_auth
def delete_instance_alarm(instance_id,
                          session=None):
    # terminate associated alarms
    alarm_response = list_instance_alarms(instance_id=instance_id)
    MetricAlarms = alarm_response['MetricAlarms']
    cloudwatch_controller = session.client('cloudwatch')
    for alarm in MetricAlarms:
        alarm_name = alarm['AlarmName']
        cloudwatch_controller.delete_alarms(AlarmNames=[alarm_name])
        # print(f'Alarm {alarm_name} deleted')


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
