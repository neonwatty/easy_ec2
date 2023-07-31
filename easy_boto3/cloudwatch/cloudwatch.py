from easy_boto3.cloudwatch.create import create_cpu_alarm
from easy_boto3.cloudwatch.list import list_alarms
from easy_boto3.cloudwatch.list import list_instance_alarms
from easy_boto3.cloudwatch.delete import delete_alarm


# centralized wiring chasis class for all current cloudwatch functionality
class Cloudwatch:
    def cloudwatch(self, sub_operation, **kwargs):
        if sub_operation == "create":
            return create_cpu_alarm(**kwargs)
        elif sub_operation == "list_all":
            return list_alarms(**kwargs)
        elif sub_operation == "list_instance":
            return list_instance_alarms(**kwargs)
        elif sub_operation == "delete":
            return delete_alarm(**kwargs)
        else:
            print("Invalid sub-operation for 'cloudwatch'")
