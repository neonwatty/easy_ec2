from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def start_instance(instance_id: str,
                   session=None) -> str:
    # create ec2 controller from session
    ec2_controller = session.client('ec2')

    # Check if instance exists
    response = ec2_controller.describe_instances(InstanceIds=[instance_id])

    # start instance if it exists
    if len(response["Reservations"]) > 0:
        # Start instance
        ec2_controller.start_instances(InstanceIds=[instance_id])

        message = f"Starting instance {instance_id}"
        print(message)
    else:
        message = f"Instance {instance_id} does not exist"
        print(message)
