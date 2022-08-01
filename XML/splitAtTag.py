import os
import xml.etree.ElementTree as ET

# THis will split at specific tags and save to a new file

# input file - full path including file and extension
f = ""

work_dir = os.path.dirname(f)
# Change to path directory
os.chdir(work_dir)

# Playing around with finding the right elements
# tree = ET.parse(f)
# root = tree.getroot()

# for law in root.iter('law'):
#     print(law.attrib['id'])

# This does the parsing and splitting work
context = ET.iterparse(f, events=('end', ))
index = 0
for event, elem in context:
    # Looking for the law tag
    if elem.tag == 'law':
        # Getting the law number from the id attribute
        lawNo = elem.attrib['id']
        filename = lawNo + ".xml"
        index += 1
        with open(filename, 'wb') as f:
            f.write(b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write(ET.tostring(elem))
