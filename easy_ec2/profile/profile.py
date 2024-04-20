from easy_ec2.profile.active import set_active_profile
from easy_ec2.profile.active import list_active_profile
from easy_ec2.profile.validation import validate
from easy_ec2.profile.validation import list_all_profiles
from easy_ec2.profile.ownership import add_ownership_data
from easy_ec2.profile.ownership import delete_ownership_data
from easy_ec2.profile.ownership import change_ownership_state
from easy_ec2.profile.ownership import change_ownership_ip


# centralized wiring chasis class for all current profile functionality
class Profile:
    def profile(self, sub_operation, **kwargs):
        if sub_operation == "add":
            return add_ownership_data(**kwargs)
        if sub_operation == "delete":
            return delete_ownership_data(**kwargs)
        if sub_operation == "change_state":
            return change_ownership_state(**kwargs)
        if sub_operation == "change_ip":
            return change_ownership_ip(**kwargs)
        if sub_operation == "validate":
            return validate(**kwargs)
        if sub_operation == "list_all":
            return list_all_profiles(**kwargs)
        if sub_operation == "set":
            return set_active_profile(**kwargs)
        if sub_operation == "list_active":
            return list_active_profile(**kwargs)
