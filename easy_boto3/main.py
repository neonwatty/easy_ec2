import fire
from .ec2.create import create_instance
from .ec2.stop import stop_instance
from .ec2.terminate import terminate_instance
from .ec2.list import list_all, list_running, list_stopped


class EasyBoto3:
    def __init__(self):
        self.create_instance = create_instance
        self.stop_instance = stop_instance
        self.terminate_instance = terminate_instance
        self.list_all = list_all
        self.list_stopped = list_stopped
        self.list_running = list_running

    def ec2(self, sub_operation, **kwargs):
        if sub_operation == "create":
            return self.create_instance(**kwargs)
        elif sub_operation == "stop":
            return self.stop_instance(**kwargs)
        elif sub_operation == "terminate":
            return self.terminate_instance(**kwargs)
        elif sub_operation == "list_all":
            return self.list_all(**kwargs)
        elif sub_operation == "list_stopped":
            return self.list_stopped(**kwargs)
        elif sub_operation == "list_running":
            return self.list_running(**kwargs)
        else:
            print("Invalid sub-operation for 'ec2'")


if __name__ == "__main__":
    fire.Fire(EasyBoto3)
