import os
import yaml 

# path to this file and parent directory
file_path = os.path.abspath(__file__)
parent_directory = '/'.join(file_path.split('/')[:-1])

 
def main():
    with open(parent_directory + '/.easy_boto3.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)
    
    
    # import log path
    with open(config, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)
    log_path = config["data"]["log_path"]



if __name__ == '__main__':
    