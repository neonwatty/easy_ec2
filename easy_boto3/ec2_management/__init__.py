import os
import sys

### add paths ###
# path to this file
file_path = os.path.abspath(__file__)

# path to this file's directory
parent_directory = '/'.join(file_path.split('/')[:-1])

# path to base directory
base_directory = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))

# add to path
sys.path.append(parent_directory)