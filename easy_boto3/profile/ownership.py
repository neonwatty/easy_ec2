
from easy_boto3 import instance_id_profile_pairs_path
from .validation import validate
import json
from easy_boto3.setup_session import setup
session_auth = setup()


def read_json_file():
    try:
        with open(instance_id_profile_pairs_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # Create an empty list if the file doesn't exist or contains invalid JSON data
    return data


def save_json_file(data):
    with open(instance_id_profile_pairs_path, 'w') as file:
        json.dump(data, file, indent=4)


def delete_entry(data, instance_id_to_delete):
    for entry in data:
        if entry["instance_id"] == instance_id_to_delete:
            data.remove(entry)
            return data
    return None


def is_instance_id_present(data, instance_id):
    for entry in data:
        if entry["instance_id"] == instance_id:
            return True
    return False


def add_running_entry(data, instance_id, public_ip, aws_profile):
    validate(aws_profile)
    if not is_instance_id_present(data, instance_id):
        new_entry = {
            "instance_id": instance_id,
            "public_ip": public_ip,
            "aws_profile": aws_profile,
            "state": "running"
        }
        data.append(new_entry)
        return data
    return None


def change_entry_state(data, instance_id, new_state='stopped'):
    for entry in data:
        if entry["instance_id"] == instance_id:
            entry["state"] = new_state
            return data
    return None


@session_auth
def add_ownership_data(instance_id: str,
                       public_ip: str,
                       profile_name: str = 'default',
                       session=None) -> None:
    # read in profile data
    data = read_json_file()

    # try to add entry to profile data
    new_data = add_running_entry(data, instance_id, public_ip, profile_name)

    # save if new_data is not None
    if new_data is not None:
        save_json_file(new_data)

    return None


@session_auth
def delete_ownership_data(instance_id: str,
                          session=None) -> None:
    # read in profile data
    data = read_json_file()

    # try to delete entry from profile data
    new_data = delete_entry(data, instance_id)

    # save if new_data is not None
    if new_data is not None:
        save_json_file(new_data)

    return None


@session_auth
def change_ownership_state(instance_id: str,
                           new_state: str = 'stopped',
                           session=None) -> None:
    # read in profile data
    data = read_json_file()

    # try to change entry state
    new_data = change_entry_state(data, instance_id, new_state)

    # save if new_data is not None
    if new_data is not None:
        save_json_file(new_data)

    return None


def list() -> list:
    # read in profile data
    data = read_json_file()

    # print all profile list
    if len(data) == 0:
        print('No profile / instsance ids')
    else:
        print(data)


def lookup_public_ip(instance_id: str) -> str:
    # read in profile data
    data = read_json_file()

    # lookup public ip
    for entry in data:
        if entry["instance_id"] == instance_id:
            return entry["public_ip"]

    return None
