from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def stop_instance(instance_id: str, 
                  session=None) -> str:
    # create ec2 controller from session
    ec2_controller = session.client('ec2')

    # check if instance is running
    response = ec2_controller.describe_instances(InstanceIds=[instance_id])
    if response['Reservations'][0]['Instances'][0]['State']['Name'] == 'running':
        # stop instance
        ec2_controller.stop_instances(InstanceIds=[instance_id])
        print(f'instance {instance_id} stopped')
    else:
        print(f'instance {instance_id} already stopped')
