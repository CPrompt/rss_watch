#!/usr/bin/python3

'''
    functions to read the json config file
    this is where we store all the info about the race
    and if it's new or not
'''

import json
import os

feedData = os.path.dirname(os.path.realpath(__file__)) + "/log/config.json"

def read_json(myFeed):
    with open(myFeed,'r') as json_file:
        data = json.load(json_file)
    return data

def output_config():
    returned_list = read_json(feedData)
    return returned_list

if __name__ == "__main__":
    motogp_title = output_config()["motogp_title"]
    print(motogp_title)
