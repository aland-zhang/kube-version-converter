#!/usr/bin/env python

import argparse
import json
import yaml
import os


def record_to_string(record, version, with_header=True):
    if with_header:
        line_pattern = "{}: {}/{}\n"
        line = line_pattern.format(version, record["Group"], record["Version"])
    else:
        line_pattern = "{}/{}"
        line = line_pattern.format(record["Group"], record["Version"])
    return line.replace("Core/", "")


def get_obj_string(object_type, k8s_version):
    if object_type in MATRIX.keys():
        obj_info = MATRIX[object_type]
        record = obj_info[k8s_version]
        return record_to_string(record, k8s_version, False)
    else:
        return False


def file_to_object(file_name):
    hdl = open(file_name, "r")
    if file_name[-1:] == "l":
        return yaml.load_all(hdl)
    else:
        obj = json.load(hdl)
        if type(obj) is dict:
            obj = [obj]
        return obj


def convert_dict(input_object, to_version):
    new_obj = {}
    # Both kind & api key in the object
    if ("kind" in input_object.keys())and("apiVersion" in input_object.keys()):
        new_version = get_obj_string(input_object["kind"], to_version)
        if new_version:
            new_obj["apiVersion"] = new_version
        else:
            new_obj["apiVersion"] = input_object["apiVersion"]
    for key in input_object.keys():
        if key == "apiVersion":
            continue
        if type(input_object[key]) is dict:
            new_obj[key] = convert_dict(input_object[key], to_version)
        elif type(input_object[key]) is list:
            new_obj[key] = convert_list(input_object[key], to_version)
        else:
            new_obj[key] = input_object[key]
    return new_obj


def convert_list(input_content, to_version):
    result_list = []
    for input_object in input_content:
        if type(input_object) is dict:
            result_list.append(convert_dict(input_object, to_version))
        elif type(input_object) is list:
            result_list.append(convert_list(input_object, to_version))
        else:
            result_list.append(input_object)
    return result_list


K8S_VER = ["1.5", "1.6", "1.7", "1.8", "1.9"]
FILE_FORMAT = ["yaml", "json"]

fi = open(os.path.join(os.path.dirname(__file__), 'matrix.json'))
MATRIX = json.load(fi)

OBJECT_LIST = MATRIX.keys()

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers()

query_parser = subparsers.add_parser(
    "query", help="Show objects in different version of Kubernetes.")
query_parser.add_argument(
    "OBJECT", metavar="[Object Type]", choices=OBJECT_LIST)

args = vars(main_parser.parse_args())
obj = MATRIX[args["OBJECT"]]
for version in obj.keys():
    record = obj[version]
    print record_to_string(record, version)
