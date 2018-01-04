#!/usr/bin/env python

import argparse
import json
import yaml
import sys
import io


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

fi = open('matrix.json')
MATRIX = json.load(fi)

OBJECT_LIST = MATRIX.keys()

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers()

query_parser = subparsers.add_parser(
    "query", help="Show objects in different version of Kubernetes.")
query_parser.add_argument(
    "OBJECT", metavar="[Object Type]", choices=OBJECT_LIST)

desc = '''
Convert Kubernetes Objects to specified Kubernetes versions.
'''
convert_parser = subparsers.add_parser("convert", help=desc)
convert_parser.add_argument("-s", "--source-file", metavar="[file name]",
                            help="YML or JSON file to process, '-' for STDIN.",
                            required=False, default="-")
convert_parser.add_argument("-d", "--dest-file", metavar="[file name]",
                            help="File name for output, '-' for STDOUT.",
                            required=False, default="-")
convert_parser.add_argument("-t", "--to-version", metavar="[output version]",
                            help="Kubernetes version of \
                            the out object file.",
                            choices=K8S_VER, required=True)
convert_parser.add_argument("-o", "--output-format",
                            metavar="[output format]",
                            help="Format of the output file, default is yaml",
                            choices=FILE_FORMAT,
                            required=False, default="yaml")

args = vars(main_parser.parse_args())

if "OBJECT" in args.keys():
    obj = MATRIX[args["OBJECT"]]
    for version in obj.keys():
        record = obj[version]
        print record_to_string(record, version)

else:
    if args["source_file"] != "-":
        obj = file_to_object(args["source_file"])
    else:
        input_lines = sys.stdin.readlines()
        input_lines = (''.join(input_lines)).decode('unicode-escape')
        first_char = input_lines[:1]
        if first_char in ["{", "[", "\""]:
            obj = json.loads(input_lines)
            if type(obj) is dict:
                obj = [obj]
        else:
            obj = yaml.load_all(io.StringIO(input_lines))
    result_content = convert_list(obj, args["to_version"])

    if args["output_format"] == "yaml":
        result_content = yaml.dump_all(
            result_content, default_flow_style=False)
    if args["output_format"] == "json":
        result_content = json.dumps(result_content, indent=True)
    if args["dest_file"] == "-":
        print result_content
    else:
        file_name = args["dest_file"]
        text_file = open(file_name, "w")
        text_file.write(result_content)
        text_file.close()
