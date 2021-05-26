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
    col_names = ["record_id", "url", "url2"]
    rows = []

    # Parsing the XML file
    tree = ET.parse(f)
    root = tree.getroot()

    for item in root:
        coll = item.find("collection/record_id").text
        slug = item.find("slug").text
        edm_is_shown_at = item.find("edm_is_shown_at/edm_is_shown_at").text

        # Add repo_coll to slug and append TN url
        record_id = coll + "_" + slug
        # url changes to thumb version
        url_rpl1 = edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://album.atlantahistorycenter.com/cdm/ref/collection/', 'https://album.atlantahistorycenter.com/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        # url changes to full download
        url2 = edm_is_shown_at.replace('http://album.atlantahistorycenter.com/cdm/ref/','https://album.atlantahistorycenter.com/digital/')

        rows.append({"record_id": record_id,
                     "url": url,
                     "url2": url2
                     })

    df = pd.DataFrame(rows, columns=col_names)

    # Writing dataframe to csv without row numbers
    df.to_csv(file_name, index=False)