import boto3


class SessionAuthenticator:
    def __init__(self, profile_name, region_name):
        self.profile_name = profile_name
        self.region_name = region_name

    def __call__(self, func):
        def decorator_function(*args, **kwargs):
            session = boto3.Session(profile_name=self.profile_name,
                                    region_name=self.region_name)
            kwargs['session'] = session
            return func(*args, **kwargs)
        return decorator_function
