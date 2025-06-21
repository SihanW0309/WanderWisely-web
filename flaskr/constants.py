import os
from pathlib import Path
import sys


cwd = Path(__file__).resolve().parents[0] # current working directory /src
project_wd = Path(__file__).resolve().parents[1]

sys.path.append(str(project_wd))

conf_wd = str(project_wd) + r'/config/'
data_wd = str(project_wd) + r'/data/'

auth_config_path = conf_wd + r'auth.yaml'
data_config_path = conf_wd + r'data.yaml'