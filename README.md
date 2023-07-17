# easy_boto3 - configuration driven AWS resource management using boto3

`easy_boto3` wraps `boto3` in an easy to use `.yaml` configuration UX for modern infrastructure-as-code usage of `boto3`, allowing for easier creation and versioning of AWS infrastructure - including deployment, management, and tear-down of AWS resources  - using familiar `boto3` syntax.

`easy_boto3` is designed to be used in conjunction with `boto3` and `awscli` to provide a simple, easy to use, and easy to refactor interface for AWS resource management.

### Contents
- [easy\_boto3 - configuration driven AWS resource management using boto3](#easy_boto3---configuration-driven-aws-resource-management-using-boto3)
    - [Contents](#contents)
  - [Installation](#installation)
  - [Using `easy_boto3` CLI](#using-easy_boto3-cli)
    - [Creating an ec2 instance with cloudwatch alarm](#creating-an-ec2-instance-with-cloudwatch-alarm)
    - [Listing ec2 instances](#listing-ec2-instances)
    - [Termianting ec2 instances by id](#termianting-ec2-instances-by-id)
  - [Using `easy_boto3`'s Python API](#using-easy_boto3s-python-api)
    - [Creating an ec2 instance](#creating-an-ec2-instance)

## Installation 

You can install `easy_boto3` via `pip` as

```bash
pip install easy_boto3
```

## Using `easy_boto3` CLI

### Creating an ec2 instance with cloudwatch alarm

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
aws_profile: <your profile name in config/credentials of ~/.aws>

ec2_instance:
  instance_details:
    InstanceName: example_worker
    InstanceType: t2.micro
    ImageId: ami-03f65b8614a860c29
    BlockDeviceMappings: 
      DeviceName: /dev/sda1
      Ebs: 
        DeleteOnTermination: true
        VolumeSize: 8
        VolumeType: gp2
    Groups:
      - <your security group>

  ssh_details: 
    KeyName: <your ssh key located in ~/.ssh>
    UserName: ubuntu
    add_to_known_hosts: true
    test_connection: true

  script_details: 
    filepath: <path_to_startup>
    inject_aws_creds: false

alarm_details:
  ComparisonOperator: GreaterThanOrEqualToThreshold
  EvaluationPeriods: 1
  MetricName: CPUUtilization
  Namespace: AWS/EC2
  Period: 60
  Statistic: Average
  Threshold: 0.99
```

Using `easy_boto3` and this configuration `config.yaml` the same task - instantiating an `ec2` instance - can be accomplished via the command line as follows:

```bash
easy_boto3 ec2 create config.yaml
```

### Listing ec2 instances 

You can use `easy_boto3` to easy see (all/ running / stopped / terminated) instances in your AWS account as follows.

See all instances

```bash
easy_boto3 ec2 list_all
```


See just running instances 

```bash
easy_boto3 ec2 list_running
```

The output of this command gives the instance id, name, type, and state of each instance in your account - looking like this

```bash
{'instance_id': 'instance_id', 'instance_state': 'running', 'instance_type': 't2.micro'}
```

You can filter by state - running, stopped, terminated - as follows

```bash
easy_boto3 ec2 list_running
```

```bash
easy_boto3 ec2 list_stopped
```

```bash
easy_boto3 ec2 list_terminated
```

### Termianting ec2 instances by id  

You can use `easy_boto3` CLI to terminate an ec2 instance by id as follows

```bash
easy_boto3 ec2 terminate <instance_id>
```

Note: by default this will delete any cloudwatch alarms associated with the instance.


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
