from easy_ec2.setup_session import setup
session_auth = setup()


@session_auth
def get_instance_public_ip(instance_id, session=None):
    # create ec2 controller from session
    ec2_controller = session.client('ec2')

    # get instance public ip
    response = ec2_controller.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['PublicIpAddress']
