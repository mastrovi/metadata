import json, os
import pandas as pd

#file = "C:\\Users\\Nicole Lawrence\\OneDrive - University of Georgia\\Documents\\Metadata\\page_json\\lccr-pages.xlsx"
file = "C:\\Users\\Nicole Lawrence\\OneDrive - University of Georgia\\Documents\\Metadata\\page_json\\gyca_gaphind-images-batch4.xlsx"
#file = input("What excel file would you like to run this on? ")
#file = input_file.strip('\"')

# File types
file_types = {'image': 'jp2',
              'pdf': 'pdf',
              'video': 'mp4',
              'audio': 'mp3'}

# Gets directory of input excel and changes to it to do work
work_dir = os.path.dirname(file)
os.chdir(work_dir)
# Gets filename then remove extension and append json
base = os.path.basename(file)
json_file = os.path.splitext(base)[0] + ".json"

# Read Excel
df = pd.read_excel(file)
col_names = {'record_id': 'id'}

# Rename columns and insert file_type
df.rename(columns=col_names, inplace=True)
df.insert(loc=1, column='file_type', value='jp2')

# Get number of items
items = len(df.index)

# Create list for row data
rows_list = []

# Get number of pages adn add row data
for item in range(items):
    slug = df.at[item, 'id']
    file_type = 'jp2'
    item_pages = {}
    for page in range(df['files'].values[item]):
        page_num = page + 1
        item_pages = {'id': slug, 'file_type': file_type, 'number': page_num}
        rows_list.append(item_pages)

# Create page level data frame
page_level_df = pd.DataFrame(rows_list)
page_level_df['number'] = page_level_df['number'].map(str)
#print(page_level_df)

# Group by id and spit out dict of id : page array
page_dict = page_level_df.groupby(['id']).apply(lambda r: r[['number']].to_dict(orient='records'))

# Add the page number column to the df and drop the file count
df['pages'] = df['id'].map(page_dict)
df.drop(columns="files", inplace=True)
#print(df)

# create a json string and load it to an object
json_str = df.to_json(orient='records')
obj = json.loads(json_str)

# Pretty print to file
with open(json_file, 'w') as f:
    json.dump(obj, f, indent=4)




