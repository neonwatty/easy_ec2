
import yaml
from easy_boto3 import internal_config_path
from easy_boto3.validation import validate
import json


def read_json_file():
    try:
        with open(internal_config_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # Create an empty list if the file doesn't exist or contains invalid JSON data
    return data


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


def add_entry(data, instance_id, aws_profile):
    validate(aws_profile)

    if not is_instance_id_present(data, instance_id):
        new_entry = {
            "instance_id": instance_id,
            "aws_profile": aws_profile
        }
        return data.append(new_entry)
    return None


def save_json_file(data):
    with open(internal_config_path, 'w') as file:
        json.dump(data, file, indent=4)
        
        
def add(instance_id: str,
        profile_name: str = 'default') -> None:
    # read in profile data
    data = read_json_file()

    # try to add entry to profile data
    new_data = add_entry(data, instance_id, profile_name)

    # save if new_data is not None
    if new_data is not None:
        save_json_file(new_data)

    return None


def delete(instance_id: str) -> None:
    # read in profile data
    data = read_json_file()

    # try to delete entry from profile data
    new_data = delete_entry(data, instance_id)

    # save if new_data is not None
    if new_data is not None:
        save_json_file(new_data)

    return None
