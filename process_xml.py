import xml.etree.ElementTree as ET
import json
import os

path = 'C:/Users/nandu/OneDrive/Documents/H2N-DEV-interview/base/'


def xml_to_dict(element):
    """
    Recursively converts an XML element and its children to a dictionary.
    """
    data_dict = {element.tag: {} if element.attrib else None}

    # Process child elements
    children = list(element)
    if children:
        child_dict = {}
        for child in children:
            child_result = xml_to_dict(child)
            if child.tag in child_dict:
                # If the tag already exists, make it a list
                if isinstance(child_dict[child.tag], list):
                    child_dict[child.tag].append(child_result[child.tag])
                else:
                    child_dict[child.tag] = [child_dict[child.tag], child_result[child.tag]]
            else:
                child_dict.update(child_result)
        data_dict[element.tag] = child_dict
    else:
        # If no child, just get the text
        data_dict[element.tag] = element.text or element.attrib
    
    return data_dict

def check_xml_file(file):
    with open(file, 'r') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        json_data = xml_to_dict(root)
    return json_data


for root, dic, files in os.walk(path):
    for file in files:
        file_name = f"{path}{file}"
        data = check_xml_file(file_name)
        #print(data)