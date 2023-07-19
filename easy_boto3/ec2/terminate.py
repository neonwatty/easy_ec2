from easy_boto3.setup_session import setup
session_auth = setup()
from easy_boto3.cloudwatch.delete import delete_instance_alarm


@session_auth
def terminate_instance(instance_id: str,
                       session=None) -> str:
    # create ec2 controller from session
    ec2_controller = session.client('ec2')

    # Check if instance exists
    response = ec2_controller.describe_instances(InstanceIds=[instance_id])

    # Terminate instance if it exists
    if len(response["Reservations"]) > 0:
        # Terminate instance
        ec2_controller.terminate_instances(InstanceIds=[instance_id])

        # Delete alarm if it exists
        delete_instance_alarm(instance_id)

        message = f"Terminating instance {instance_id} along with any associated cpu alarms"
        print(message)
    else:
        message = f"Instance {instance_id} does not exist"
        print(message)
