#pip install pyyaml
import yaml
from pprint import pprint

with open("yaml_example.yaml", "r") as f:
    yaml_dict = yaml.safe_load(f)


pprint(yaml_dict)

