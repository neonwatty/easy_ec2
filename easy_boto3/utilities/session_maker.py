import functools
import boto3
from easy_boto3.utilities.logger_maker import LogExceptions


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
