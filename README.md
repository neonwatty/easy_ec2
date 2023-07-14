# easy_boto3 - configuration driven AWS resource management using boto3

`easy_boto3` wraps `boto3` in an easy to use `.yaml` configuration UX for modern infrastructure-as-code usage of `boto3`, allowing for easier creation and versioning of AWS infrastructure - including deployment, management, and tear-down of AWS resources  - using familiar `boto3` syntax.

`easy_boto3` is designed to be used in conjunction with `boto3` and `awscli` to provide a simple, easy to use, and easy to refactor interface for AWS resource management.

[Installation](#installation) 
[Getting started](#getting-started)
[Example usage](#example-usage) 
[Using `easy_boto3`'s Python API](#using-easy_boto3s-python-api)

## Installation 

You can install `easy_boto3` via `pip` as

```bash
pip install easy_boto3
```

## Using `easy_boto3`

`easy_boto3` allows you to translate a standard `boto3` pythonic infrastructure task like instantiating an `ec2` instance with an attached `cloudwatch` cpu usage alarm from complex pythonic implementation like the following 

```python
import boto3

# read in aws_access_key_id and aws_secret_access_key based on input profile_name using boto3
session = boto3.Session(profile_name=profile_name)

# create ec2 controller from session
ec2_controller = session.resource('ec2')

# read in startup script
with open(startup_script_path, 'r') as file:
    startup_script = file.read()

# create a new EC2 instance
instances = ec2_controller.create_instances(
    ImageId='ami-03f65b8614a860c29',
    InstanceName='example_worker',
    NetworkInterfaces=[{
        'DeviceIndex': 0,
        'Groups': ['sg-1ed8w56f12347f63d'],
        'AssociatePublicIpAddress': True}],
    UserData=startup_script,
    TagSpecifications=[{'ResourceType': 'instance',
                        'Tags': [{'Key': 'Name', 'Value': 'example_worker'}]}],
    InstanceType='t2.micro',
    KeyName=<ssh_key_name>,
    )

# wait for the instance to enter running state
instances[0].wait_until_running()
instance_id = instances[0].id

# create cloud watch client
cloudwatch_client = session.client('cloudwatch')

# enable detailed monitoring for the instance
ec2_client.monitor_instances(InstanceIds=[instance_id])

# create alarm
result = cloudwatch_client.put_metric_alarm(
        AlarmName=cpu_alarm_name,
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        EvaluationPeriods=1,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=60,
        Statistic='Average',
        Threshold=threshold_value,
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ],
    )
```

into easier to re / use and refactor `.yaml` configuration file using the same `boto3` option syntax for to declaration of the same task.  So for example the above task can be accomplished using the analogous `.yaml` configuration file carrying over the same `boto3` option syntax as follows:

```yaml
awsProfile: profile_name

createEc2Instance:
    InstanceName: example_worker
    region: us-west-2
    InstanceType: t2.micro
    ImageId: ami-03f65b8614a860c29
    Tags: 
        - key: Name
        value: example_worker
    NetworkInterfaces:
        - DeviceIndex: 0
          Groups: 
            - sg-1ed8w56f12347f63d
          AssociatePublicIpAddress: true
    KeyName: <ssh_key_name>
    TagSpecifications: 
        - ResourceType: instance
            Tags: 
            - key: Name
                value: example_worker
    startupScript: 
        filePath: path_to_startup_script

createCloudWatchAlarm:
    AlarmName: ccpu_alarm_name
    ComparisonOperator: GreaterThanOrEqualToThreshold
    EvaluationPeriods: 1
    MetricName: CPUUtilization
    Namespace: AWS/EC2
    Period: 60
    Statistic: Average
    Threshold: threshold_value
    Dimensions:
        - Name: InstanceId
          Value: {{createEc2Instance.InstanceId}}
```

Using `easy_boto3` and this configuration `config.yaml` the same task - instantiating an `ec2` instance - can be accomplished via the command line as follows:

```python
easy_boto3 --config /path/to/config.yaml
```

Further infrastructure configuration examples can be found in the `examples/command_line` directory.

## Using `easy_boto3`'s Python API

In addition to config driven command line use, `easy_boto3` also offers a simplified python API that makes creating and managing AWS resources with `boto3` easier.

### Creating an ec2 instance 

In this example an ec2 instance of user-specified type and AMI is created.

Note `block_device_mappings` and `UserData` startup bash script are optional.

```python
from easy_boto3 import set_profile
from easy_boto3.startup_script_management import read_startup_script
from easy_boto3.ec2_instance_management import launch_instance

# set aws profile - optional - set to 'default' profile by default
set_profile.set('my_aws_profile') # -> returns None if profile is valid

# read in startup script from file
UserData = read_startup_script('./path/to/startup.sh')

# build ec2 launch instance command
InstanceName = 'example_worker'
InstanceType = 't2.micro'
ImageId = 'ami-03f65b8614a860c29'
Groups = ['my_security_group_id']
BlockDeviceMappings = [
    {
        'DeviceName': '/dev/sda1',
        'Ebs': {
            'VolumeSize': 300,
            'VolumeType': 'gp2'
        }
    }
]
KeyName = 'my_ssh_key_name'

# launch instance
launch_result = launch_instance(KeyName=KeyName,
                                InstanceName=InstanceName,
                                InstanceType=InstanceType,
                                ImageId=ImageId,
                                Groups=Groups,
                                BlockDeviceMappings=BlockDeviceMappings,
                                UserData=UserData)

# wait for the instance to enter running state
launch_result.wait_until_running()

# get instance id
instance_id = launch_result[0].id
```
Further uses of the Python API can be found in the `examples/python_api` directory.
