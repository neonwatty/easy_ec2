import fire
from .ec2.create import create_instance
from .ec2.stop import stop_instance
from .ec2.terminate import terminate_instance
from .ec2.list import list_all, list_running, list_stopped
from .cloudwatch.create import create_cpu_alarm
from .cloudwatch.list import list_alarms
from .cloudwatch.delete import delete_alarm


class EasyBoto3:
    def __init__(self):
        self.create_instance = create_instance
        self.stop_instance = stop_instance
        self.terminate_instance = terminate_instance
        self.list_all_instances = list_all
        self.list_stopped_instances = list_stopped
        self.list_running_instances = list_running

        self.create_cpu_alarm = create_cpu_alarm
        self.list_all_alarms = list_alarms
        self.delete_alarm = delete_alarm

    def ec2(self, sub_operation, **kwargs):
        if sub_operation == "create":
            return self.create_instance(**kwargs)
        elif sub_operation == "stop":
            return self.stop_instance(**kwargs)
        elif sub_operation == "terminate":
            return self.terminate_instance(**kwargs)
        elif sub_operation == "list_all":
            return self.list_all_instances(**kwargs)
        elif sub_operation == "list_stopped":
            return self.list_stopped_instances(**kwargs)
        elif sub_operation == "list_running":
            return self.list_running_instances(**kwargs)
        else:
            print("Invalid sub-operation for 'ec2'")

    def cloudwatch(self, sub_operation, **kwargs):
        if sub_operation == "create":
            return self.create_cpu_alarm(**kwargs)
        elif sub_operation == "list":
            return self.list_all_alarms(**kwargs)
        elif sub_operation == "delete":
            return self.delete_alarm(**kwargs)
        else:
            print("Invalid sub-operation for 'cloudwatch'")


if __name__ == "__main__":
    fire.Fire(EasyBoto3)
