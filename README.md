# easy_boto3 - a simpler way of managing AWS resources via boto3

`easy_boto3` reduces the complexity of using bare metal `boto3` by adding useful abstractions on top of it that make it easier to employ in creating, managing, and tearing down AWS resources. 

To get started you just need to direct `easy_boto3` to your locally stored AWS credentials, desired profile, and AWS-specific ssh key.  Do this by creating a simple config file where you store your `aws` credentials at `~/.aws/easy_boto3/easy_boto3_base.yaml` in the simple format shown below.

```yaml
aws_data:
    aws_config_directory: <path_to_your_aws_config> -> typically something like: /Users/<my_user>/.aws
    profile_name: <your_desired_aws_profile>
    aws_ssh_key: <path_to_your_ssh_key> -> typically something like: /Users/<my_user>/.ssh/<your_aws_key>
```




## Installation

```bash
pip install easy_boto3
```

## Example usage
### examples - creating an ec2 instance 

In this example an ec2 instance of user-specified type and AMI is created using a user-defined startup `bash` script.  

```python 
from easy_boto3.ec2_instance_management import launch_instance

# define basic parameters of ec2 instance - including instance type and ami
region = 'us-west-2'
InstanceName = 'example_worker'
InstanceType = 't2.micro'
ImageId = 'ami-03f65b8614a860c29'
    
# launch instance
launch_response = launch_instance(region=region,
                                  InstanceName=InstanceName,
                                  InstanceType=InstanceType,
                                  ImageId=ImageId)

```

In this example we add to the previous by passing a user defined `bash` startup script that will be executed when the ec2 instance is first instantiated.


```python
from easy_boto3.startup_script_management import read_startup_script
from easy_boto3.ec2_instance_management import launch_instance

# read in startup script from file
startup_script = read_startup_script(<path_to_startup_script>)

# define basic parameters of ec2 instance - including instance type and ami
region = 'us-west-2'
InstanceName = 'example_worker'
InstanceType = 't2.micro'
ImageId = 'ami-03f65b8614a860c29'
    
# launch instance
launch_response = launch_instance(region=region,
                                  InstanceName=InstanceName,
                                  InstanceType=InstanceType,
                                  ImageId=ImageId,
                                  startup_script=startup_script)

```

In this example we add to the previous example, showing special functionality for injecting AWS credentials into the `bash` startup script.  This allows for easy AWS login on the instantiated ec2 instance without storing AWS credentials themselves in the startup script.

To use this feature, simply add variables `$aws_access_key_id` and `$aws_secret_access_key` to your `bash` startup script as shown below.

```bash
#!/bin/bash
sudo apt-get update
sudo apt-get install -y awscli

# Set AWS access key ID and secret access key using the AWS CLI
sudo aws configure set aws_access_key_id $aws_access_key_id
sudo aws configure set aws_secret_access_key $aws_secret_access_key
```

Then `easy_boto3` takes care of credential injection as shown below (using the path set in your `~/.easy_boto3/easy_boto3_base.yaml` config)

```python
from easy_boto3.startup_script_management import read_startup_scriptinject_aws_creds
from easy_boto3.ec2_instance_management import launch_instance

# read in startup script from file
startup_script = read_startup_script(<path_to_startup_script>)

# inject aws creds into base script
startup_script = inject_aws_creds(startup_script)

# define basic parameters of ec2 instance - including instance type and ami
region = 'us-west-2'
InstanceName = 'example_worker'
InstanceType = 't2.micro'
ImageId = 'ami-03f65b8614a860c29'
    
# launch instance
launch_response = launch_instance(region=region,
                                  InstanceName=InstanceName,
                                  InstanceType=InstanceType,
                                  ImageId=ImageId,
                                  startup_script=startup_script)

```