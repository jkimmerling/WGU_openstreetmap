import csv


def populate_parent_list(tag_type, tag_type_list, values, parent):
    # Force correct types on all data, this will avoid need to validate vs the schema
    tag_type['id'] = int(values['id'])
    if parent == "node":
        tag_type['lat'] = float(values['lat'])
        tag_type['lon'] = float(values['lon'])
    tag_type['user'] = str(values['user'])
    tag_type['uid'] = int(values['uid'])
    tag_type['version'] = str(values['version'])
    tag_type['changeset'] = int(values['changeset'])
    tag_type['timestamp'] = str(values['timestamp'])
    tag_type_list.append(tag_type)



def split_values(values_to_split, character_to_split, subs_list):
    # Split up the values that have certain characters, check them vs the abbrevication list, 
    # and join them back together once fixed or cleared
    temp_list = values_to_split.split(character_to_split)
    new_list = []
    for temp_value in temp_list:
        if temp_value in subs_list.keys():
            new_list.append(str(subs_list.get(temp_value)))
        else:
            new_list.append(str(temp_value))
    cleaned_value_tag_list = character_to_split.join(new_list)
    return cleaned_value_tag_list



def populate_parent_tag_list(tag_type, tag_type_list, values, parent, subs_list):
    # Force correct types on all data, this will avoid need to validate vs the schema
    tag_type['id'] = int(parent['id'])
    tag_type['key'] = str(values['k'])
    tag_type['value'] = ""
    tag_type['type'] = "default"

    # swap bad abbreviations, get rid of bad characters, remove overlapping info
    cleaned_value_tag = ""
    if ":" in values['v']:
        tag_type['value'] = split_values(values['v'], ":", subs_list)
    elif "," in values['v']:
        tag_type['value'] = split_values(values['v'], ",", subs_list)
    elif ";" in values['v']:
        tag_type['value'] = split_values(values['v'], ";", subs_list)
    else:
        if values['v'] in subs_list.keys():
            cleaned_value_tag = subs_list.get(values['v'])
            tag_type['value'] = str(cleaned_value_tag)
        else:
            tag_type['value'] = values['v']

    # Sort out the types and keys
    if ":" in values['k']:
        split_tag = values['k'].split(":")
        if len(split_tag) > 2:
            tag_type['type'] = str(split_tag[0])
            tag_type['key'] = ":".join(split_tag[1:])
        else:
            tag_type['type'] = str(split_tag[0])
            tag_type['key'] = str(split_tag[1])
    else:
        tag_type['key'] = str(values['k'])
    tag_type_list.append(tag_type)



def push_to_csv(file_name, list_to_push):
    # Write each csv file using the list of dictionaries. Uses the dictionary keys to populate the header
    # fields of the csv
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list_to_push[0].keys())
        writer.writeheader()
        for node in list_to_push:
            writer.writerow(node)