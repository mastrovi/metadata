import json, os
import pandas as pd

file = input("What excel file would you like to run this on? ")
file = file.strip('\"')

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

# Read all sheets from Excel file and flatten result
df = pd.read_excel(file, sheet_name=None)
page_level_df = pd.concat(df.values(), keys=df.keys())
page_level_df = page_level_df.reset_index(level=[0])

# Rename columns and insert file_type
col_names = {'level_0': 'id', 'image': 'number', 'page': 'title'}
page_level_df.rename(columns=col_names, inplace=True)
page_level_df['number'] = page_level_df['number'].map(str)
page_level_df['title'] = page_level_df['title'].map(str)

# Create record_id column and file_type column in final items_df
record_ids = list(df.keys())
items_df = pd.DataFrame(record_ids, columns=['id'])
items_df.insert(loc=1, column='file_type', value='jp2')

# Group by id and spit out page/title
page_dict = page_level_df.groupby(['id']).apply(lambda r: r[['number', 'title']].to_dict(orient='records'))

# Add the page number/title dict as a column to the items_df
items_df['pages'] = items_df['id'].map(page_dict)
print(items_df)
#
# create a json string and load it to an object
json_str = items_df.to_json(orient='records')
obj = json.loads(json_str)

# Pretty print to file
with open(json_file, 'w') as f:
    json.dump(obj, f, indent=4)




