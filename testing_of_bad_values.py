
map_file_open = open(mapfile, "rb")
node_types = set()
street_names = set()
tiger_tags = set()
tiger_values = defaultdict(set)
tiger_names = set()
direction_tags = set()
street_type_tags = set()
unsorted_tags = set()
zip_codes = set()

if "tiger:zip" in tag.attrib['k']:
    if len(tag.attrib['v']) > 5:
        print(tag.attrib['v'])

                if len(way_tag['value']) < 4:
                    print(way_tag['value'])