from easy_boto3 import active_profile_path
import json


def read_json_file():
    try:
        with open(active_profile_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    return data


def save_json_file(data):
    with open(active_profile_path, 'w') as file:
        json.dump(data, file, indent=4)


def set_active_profile(profile_name: str = 'default') -> None:
    # read in profile data
    data = read_json_file()

    # update profile data
    data = {'active_profile': profile_name}

    # save profile data
    save_json_file(data)

    # print confirmation
    print('')
    print('active profile now set to:')
    print('---------------')
    print(profile_name)
    print('')


def list_active_profile() -> list:
    # read in profile data
    data = read_json_file()

    # print active profile list
    if len(data) == 0:
        print('No active profile set')
    else:
        # print out active profile
        print('')
        print('active profile:')
        print('---------------')
        print(data['active_profile'])
        print('')
