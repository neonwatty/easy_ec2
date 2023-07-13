# easy_boto3 - a simpler way of managing AWS resources via boto3

`easy_boto3` wraps `boto3` in an easy to use `.yaml` configuration UX for modern infrastructure-as-code usage of `boto3`.  This allows for easier auditing and iteration of AWS infrastructure; deployment, management, and tear-down of AWS resources; and provides more `boto3` fine-tuning options compared to config systems like `terraform`.

## Installation

You can install `easy_boto3` via `pip` as

```bash
pip install easy_boto3
```

## Getting started

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

Note `block_device_mappings` are optional.

```python 
from easy_boto3.ec2_instance_management import launch_instance

# ssh key_name for instance creation - note you only need the name here (not the path)
key_name = <ssh_key_name>

# define basic parameters of ec2 instance - including instance type and ami
region = 'us-west-2'
instance_name = 'example_worker'
instance_type = 't2.micro'
image_id = 'ami-03f65b8614a860c29'
security_group_ids = [<security_group_id>]
block_device_mappings = [<your_block_device_mappings>] # optional

    
# launch instance
launch_response = launch_instance(key_name=key_name,
                                  region=region,
                                  instance_name=instance_name,
                                  instance_type=instance_type,
                                  image_id=image_id,
                                  security_group_ids=security_group_ids,
                                  block_device_mappings=block_device_mappings)

```

In this example we add to the previous by passing a user defined `bash` startup script that will be executed when the ec2 instance is first instantiated.


```python
from easy_boto3.startup_script_management import read_startup_script
from easy_boto3.ec2_instance_management import launch_instance

# ssh key_name for instance creation - note you only need the name here (not the path)
key_name = <ssh_key_name>

# read in startup script from file
startup_script = read_startup_script(<path_to_startup_script>)

# define basic parameters of ec2 instance - including instance type and ami
region = 'us-west-2'
instance_name = 'example_worker'
instance_type = 't2.micro'
image_id = 'ami-03f65b8614a860c29'
security_group_ids = [<security_group_id>]

# launch instance
launch_response = launch_instance(key_name=key_name,
                                  region=region,
                                  instance_name=instance_name,
                                  instance_type=instance_type,
                                  image_id=image_id,
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

# ssh key_name for instance creation - note you only need the name here (not the path)
key_name = <ssh_key_name>

# read in startup script from file
startup_script = read_startup_script(<path_to_startup_script>)

# inject aws creds into base script
startup_script = inject_aws_creds(startup_script)

# define basic parameters of ec2 instance - including instance type and ami
region = 'us-west-2'
instance_name = 'example_worker'
instance_type = 't2.micro'
image_id = 'ami-03f65b8614a860c29'
security_group_ids = [<security_group_id>]

# launch instance
launch_response = launch_instance(key_name=key_name,
                                  region=region,
                                  instance_name=instance_name,
                                  instance_type=instance_type,
                                  image_id=image_id,
                                  startup_script=startup_script,
                                  security_group_ids=security_group_ids)
```


## Setting profile

You can easily validate, check, and change between AWS profiles using `easy_boto3`.

By default `easy_boto3` uses your `default` profile.

```python 
from easy_boto3 import set_profile

# validate current profile
set_profile.validate() # -> returns None if profile valid

# check which profile is currently being used - automatically validates
set_profile.check()  # -> 'default'

# set new profile - automatically validates new profile
set_profile.validate('your_alternative_profile') # -> returns None if profile is valid

```

Note: to use an alternative profile `set_profile.set` must be run first.

For example, to use `your_alternative_profile` to launch an ec2 instance:

```python
# set alternative aws profile
from easy_boto3 import set_profile
set_profile.validate('your_alternative_profile')

# launch an ec2 instance under this alternative profile
from easy_boto3.ec2_instance_management import launch_instance

# ssh key_name for instance creation - note you only need the name here (not the path)
key_name = <ssh_key_name>

# define basic parameters of ec2 instance - including instance type and ami
region = 'us-west-2'
instance_name = 'example_worker'
instance_type = 't2.micro'
image_id = 'ami-03f65b8614a860c29'
security_group_ids = [<security_group_id>]

# launch instance
launch_response = launch_instance(key_name=key_name,
                                  region=region,
                                  instance_name=instance_name,
                                  instance_type=instance_type,
                                  image_id=image_id,
                                  security_group_ids=security_group_ids)
```