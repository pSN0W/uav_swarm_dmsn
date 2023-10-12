import yaml

CONFIG_FILE_LOC="../config.yaml"

with open(CONFIG_FILE_LOC, 'r') as f:
    CONFIG = yaml.safe_load(f)
