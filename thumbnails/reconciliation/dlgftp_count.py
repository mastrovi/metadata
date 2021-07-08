collections = dict()

with open("C:\\Users\\Nicole Lawrence\\Desktop\\thumbnails\\thumbnails_20210622_edit.txt", "r") as file:
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

with open('C:\\Users\\Nicole Lawrence\\Desktop\\thumbnails\\collection_thumb_counts.txt', 'w') as f:
    print(collections, file=f)