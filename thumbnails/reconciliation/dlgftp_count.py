import os

collections = dict()

input_file = input("Input the path to the thumbnail tree: ")
input_file = input_file.strip('\"')

work_dir = os.path.dirname(input_file)
# Gets filename without extension
base = os.path.basename(input_file)
# Appends filename to directory path
new_file = work_dir + '/collection_thumb_counts.txt'

with open(input_file, "r") as file:
    for line in file.readlines():
        if (line.find('_') != -1):
            coll, value = line.rsplit("_", 1)
            value.strip()  # Strip the new line character
            if (coll in collections):  # Test to see if we see this line before
                collections[coll] += 1  # augmented addition operator
            else:
                collections[coll] = 1   # line not found assign basic value
                print("Counting ", coll)
        else:
            pass

with open(new_file, 'w') as f:
    print(collections, file=f)
