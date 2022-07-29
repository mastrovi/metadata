import xml.etree.ElementTree as ET

'''
Useful if your originating XML is huge and and you can't format it in a text editor
'''

# input file - full path including file and extension
f = ""
#output file - full path including file and extension, doesn't have to exist yet
file_name = ""

def _pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))

tree = ET.parse(f)
root = tree.getroot()

_pretty_print(root)

tree = ET.ElementTree(root)
tree.write(file_name)
# Uncomment below to see output in console
#with open(file_name, 'r') as f:
#    print(f.read())