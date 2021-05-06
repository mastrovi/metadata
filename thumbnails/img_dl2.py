# Importing the required libraries
import os
import xml.etree.ElementTree as ET
import pandas as pd

path = input('What directory would you like to run this on? ')
# Change to path directory
os.chdir(path)

# Find files
files = [fi for fi in os.listdir(path) if fi.endswith('.xml')]

# Do work
for f in files:
    file_name = os.path.splitext(f)[0] + ".csv"
    print("Converting ", file_name)
    col_names = ["record_id", "url"]
    rows = []

    # Parsing the XML file
    tree = ET.parse(f)
    root = tree.getroot()

    # Do url prefix replacement
    for elem in root.iter():
        try:
        # AUU replacement
          elem.text = elem.text.replace('http://hdl.handle.net/20.500.12322/', 'https://radar.auctr.edu/islandora/object/')
        except AttributeError:
          pass

    for item in root:
        coll = item.find("collection/record_id").text
        slug = item.find("slug").text
        edm_is_shown_at = item.find("edm_is_shown_at/edm_is_shown_at").text

        # Add repo_coll to slug and append TN url
        record_id = coll + "_" + slug
        # AUU addendum
        url = edm_is_shown_at + "/datastream/TN/view"

        rows.append({"record_id": record_id,
                     "url": url,
                     })

    df = pd.DataFrame(rows, columns=col_names)

    # Writing dataframe to csv without row numbers
    df.to_csv(file_name, index=False)
