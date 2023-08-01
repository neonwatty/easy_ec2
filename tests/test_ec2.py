from pathlib import Path
import sys
current_dir = Path(__file__).parent.__str__()
parent_dir = Path(__file__).parent.parent.__str__()
sys.path.append(parent_dir)
test_config_path = current_dir + '/test_configs/small_test.yaml'
main_path = parent_dir + '/easy_boto3/main.py'

from io import StringIO
from unittest.mock import patch
from easy_boto3.main import main


# def test_ec2_list_all():
#     # call main for ec2 list_all test
#     result = main('easy_boto3', 'ec2', 'list_all')
#     if result is not None:
#         assert True
#     else:
#         assert False


# def test_ec2_list_running():
#     # call main for ec2 list_running test
#     result = main('easy_boto3', 'ec2', 'list_running')
#     if result is not None:
#         assert True
#     else:
#         assert False


# def test_ec2_list_stopped():
#     # call main for ec2 list_stopped test
#     result = main('easy_boto3', 'ec2', 'list_stopped')
#     if result is not None:
#         assert True
#     else:
#         assert False

def test_ec2_stop(instance_id):
    # call main for ec2 stop test
    result = main('easy_boto3', 'ec2', 'stop', instance_id)
    if result is not None:
        assert True
    else:
        assert False

# def test_ec2_create():
#     # call main for ec2 create test
#     result = main('easy_boto3', 'ec2', 'create', test_config_path)
#     print(f'result: {result}')
#     if result is not None:
#         instance_id = result['instance_id']
        
#         assert True
#     else:
#         assert False


# def test_ec2_create():
#     # Simulate command line arguments
#     args = ["ec2", "create", f"{test_config_path}"]

#     # Patch the 'sys.argv' with the simulated command line arguments
#     with patch("sys.argv", [main_path] + args):
#         # Redirect stdout to capture the output
#         with patch("sys.stdout", new=StringIO()) as fake_out:
#             # Call the main function
#             main()

#             # Get the output
#             output = fake_out.getvalue()
#             print(output)

#             # Assert the expected output or behavior
#             assert output == "Expected Output"

# test_ec2_create()