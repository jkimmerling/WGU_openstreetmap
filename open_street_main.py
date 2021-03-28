import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import processing_funcs as pf
import os
import csv


# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="jasonk",
# #   password="This is my linux password"
# )

# print(mydb)

# empty lists that will be filled by the relevent steps
node_list = []
way_list = []
way_tag_list = []
node_tag_list = []
way_node_list = []

# Dictionary to help iterate through the csv generation step
cvs_dict = {
    "nodes.csv": node_list, 
    "ways.csv": way_list,
    "way_tags.csv": way_tag_list, 
    "node_tags.csv": node_tag_list, 
    "way_node_connections.csv": way_node_list
}

# List of abbreviations that will need to be swapped to the full word
subs = {
    "Ln": "Lane",
    "Rd": "Road",
    "Dr": "Drive", 
    "Trl": "Trail",
    "Ct": "Court",
    "Ave": "Avenue",
    "St": "Street",
    "Pl": "Place",
    "Hwy": "Highway",
    "N": "North",
    "W": "West",
    "S": "South",
    "E": "East",
    "NE": "Northeast",
    "NW": "Northwest",
    "SE": "Southeast",
    "SW": "Southwest",
    "GA": "Georgia",
    " GA": " Georgia",
    "Ga": "Georgia"
}

# Preoblem character regexp search provided by udacity
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Get the path of the xml file and open it
cwd = os.getcwd()
mapfile = cwd + "/gordon_county.xml"
map_file_open = open(mapfile, "rb")

# Iterate through all of the tags fields in the xml file
for event, elem in ET.iterparse(map_file_open, events=("start",)):

    if elem.tag == "node":
        # Set the empty disctionary for the node
        node = {}
        pf.populate_parent_list(node, node_list, elem.attrib, elem.tag)

        # Node tags needed: id, key, value, type
        for tag in elem.iter("tag"):  
            
            # If the tag is a "tag", then skip it if it has problem characters, or add it to the node_tag_list
            if PROBLEMCHARS.search(tag.attrib['k']):
                print(tag.attrib['k'])
                continue
            else:            
                node_tag = {}
                pf.populate_parent_tag_list(node_tag, node_tag_list, tag.attrib, node, subs) 

    if elem.tag == "way":
        # Set the empty dictionaries for the way and the "way + node " relation
        way = {}
        way_node = {}
        pf.populate_parent_list(way, way_list, elem.attrib, elem.tag)

        # Set a counter for the "nd" tags, as this will mark their position
        counter = 0

        # Cycle through the child tags under the "way"
        for tag in elem:

            # if the tag is a nd, process it and add it to the way_node_list
            if tag.tag == "nd":  
                way_node = {}
                way_node['id'] = int(way['id'])
                way_node['node_id'] = int(tag.attrib['ref'])
                way_node['position'] = int(counter)
                way_node_list.append(way_node)
                counter += 1

            # If the tag is a "tag", then skip it if it has problem characters, or add it to the way_tag_list
            if tag.tag == "tag": 
                if PROBLEMCHARS.search(tag.attrib['k']):
                    print(tag.attrib['k'])
                    continue
                else:                        
                    way_tag = {}     
                    pf.populate_parent_tag_list(way_tag, way_tag_list, tag.attrib, way, subs)     

# Close the file to avoid memory leaks or other issues
map_file_open.close()

# Iterate through the csv_dict to generate the csv files needed to populate the DB
for file_name, list_to_push in cvs_dict.items():
    pf.push_to_csv(file_name, list_to_push)
