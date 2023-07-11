import functools
import boto3
import botocore


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
            try:
                result = func(*args, **kwargs)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'UnauthorizedOperation':
                    decoded_message = self.decode_authorization_failure_message(e.response['Error']['Message'])
                    print(f"FAILURE: {func_name} failed: {e}\nDecoded message: {decoded_message}")
                else:
                    print(f"FAILURE: {func_name} failed: {e}")
            except Exception as e:
                print(f"FAILURE: {func_name} failed: {e}")
            else:
                print(f"SUCCESS: {func_name} succeeded")
                return result
        return wrapper


class SessionAuthenticator:
    def __init__(self, 
                 aws_access_key_id,
                 aws_secret_access_key,
                 aws_profile_name,
                 aws_region_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = aws_region_name
        self.profile_name = aws_profile_name
        self.log_exceptions = LogExceptions()

    def __call__(self, func):
        @self.log_exceptions
        @functools.wraps(func)
        def decorator_function(*args, **kwargs):
            session = boto3.Session(aws_access_key_id=self.aws_access_key_id,
                                    aws_secret_access_key=self.aws_secret_access_key,
                                    profile_name=self.profile_name,
                                    region_name=self.region_name)
            kwargs['session'] = session
            return func(*args, **kwargs)
        return decorator_function
