import functools
import boto3
import botocore
from yaspin import yaspin


def decode_authorization_failure_message(message):
    sts_client = boto3.client('sts')
    response = sts_client.decode_authorization_message(EncodedMessage=message)
    return response['DecodedMessage']


class LogExceptions:
    def __init__(self):
        # self.file_path = file_path
        self.decode_authorization_failure_message = decode_authorization_failure_message

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            with yaspin(text=f"executing {func_name}", color="yellow") as spinner:
                try:
                    result = func(*args, **kwargs)
                except botocore.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'UnauthorizedOperation':
                        decoded_message = self.decode_authorization_failure_message(e.response['Error']['Message'])
                        print(f"FAILURE: {func_name} failed: {e}\nDecoded message: {decoded_message}")
                        spinner.fail("💥 ")
                    else:
                        print(f"FAILURE: {func_name} failed: {e}")
                        spinner.fail("💥 ")
                except Exception as e:
                    spinner.fail("💥 ")
                    print(f"FAILURE: {func_name} failed: {e}")
                else:
                    # print(f"SUCCESS: {func_name} succeeded")
                    spinner.ok("✅ SUCCESS: ")
                    return result
        return wrapper


class SessionAuthenticator:
    def __init__(self,
                 aws_access_key_id,
                 aws_secret_access_key,
                 aws_region_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = aws_region_name
        self.log_exceptions = LogExceptions()

    def __call__(self, func):
        @self.log_exceptions
        @functools.wraps(func)
        def decorator_function(*args, **kwargs):
            session = boto3.Session(aws_access_key_id=self.aws_access_key_id,
                                    aws_secret_access_key=self.aws_secret_access_key,
                                    region_name=self.region_name)
            kwargs['session'] = session
            return func(*args, **kwargs)
        return decorator_function
