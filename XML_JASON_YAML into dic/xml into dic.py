
import xmltodict
from pprint import pprint

xml_example = open ("xml_example.xml").read()

xml_dict = xmltodict.parse(xml_example)

pprint(xml_dict)
