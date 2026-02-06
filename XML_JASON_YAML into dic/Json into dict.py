import json

from pprint import pprint

jason_example = open("Json_example.json").read()

jason_dict = json.loads(jason_example)

pprint (jason_dict)

