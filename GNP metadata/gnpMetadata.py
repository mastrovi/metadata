import os, datetime
import pandas as pd

titles ={'sn90052391' : "The Banks County News"
}

# Dictionary of tiles using LCCN ad the key
locations = {'sn90052391' : "Douglasville GA"
}

# Ask for file
input_file = input("What excel file would you like to run this on? ")
file = input_file.strip('\"')



# Gets directory of input excel and changes to it to do work
work_dir = os.path.dirname(file)
os.chdir(work_dir)

# Gets filename, remove extension and append metadata.xslx, create batchID from filename
base = os.path.basename(file)
metadata_file = os.path.splitext(base)[0] + "_metadata.xlsx"
xml_file = os.path.splitext(base)[0] + ".xml"
batch_file = os.path.splitext(base)[0] + "_rename.bat"
batchID = os.path.splitext(base)[0]

# Read Excel
df = pd.read_excel(file)
col_names = {'Vol #' : 'Volume_Number', 'Issue #' : 'Issue_Number', 'Number of Pages' : 'Number_of_Pages'}

# Rename columns and insert fields
df.rename(columns=col_names, inplace=True)
df.insert(loc=2, column='Title', value='')
df.insert(loc=3, column='Standard_Title', value='')
df.insert(loc=4, column='LCCN', value='')
df.insert(loc=5, column='Date', value='')
df.insert(loc=6, column='Date-Numeric', value='')
df.insert(loc=10, column='Edition_Order', value='1')
df.insert(loc=11, column='Page_Sequence_Number', value='')
df.insert(loc=12, column='Page_Physical_Description', value='Print')
df.insert(loc=13, column='Frame_ID', value='')
df.insert(loc=14, column='Issue_ID', value='')
df.insert(loc=15, column='Reproduction_Agency', value='Digital Library of Georgia; Athens GA')
df.insert(loc=16, column='Reproduction_Agency_Code', value='gu')
df.insert(loc=17, column='Reproduction_Note', value='Present')
df.insert(loc=18, column='Physical_Location', value='Georgia Newspaper Project; Athens GA')
df.insert(loc=19, column='Physical_Location_Code', value='gnp')
df.insert(loc=20, column='Batch_Name', value='')
df.insert(loc=21, column='Reel_Number', value='')
df.insert(loc=22, column='Reel_Sequence_Number', value='')
df.insert(loc=23, column='Digital_Filename', value='')
df.insert(loc=24, column='File_Rename', value='')

# Get number of items
items = len(df.index)

# Create list for row data
rows_list = []

# Get number of pages and add row data
for item in range(items):
    df['Date'] = df['Issue Date'].dt.strftime('%B %#d, %Y')
    df['Date-Numeric'] = df['Issue Date'].dt.strftime('%Y-%m-%d')
    df['LCCN'] = df['ISSUE_NO'].str.partition('_')[0]
    df['Issue_ID'] = df['ISSUE_NO']
    df['Batch_Name'] = batchID
    df['Reel_Number'] = batchID
    lccn = df.at[item, 'LCCN']
    df['Standard_Title'] = titles[lccn]
    df['Title'] = titles[lccn] + " [" + locations[lccn] + ", " + df.at[item, 'Date'] + "]"

#    slug = df.at[item, 'id']
    item_pages = {}
    for page in range(df['Number_of_Pages'].values[item]):
        page_num = page + 1
        issue_id = batchID + "_" + df.at[item, 'Date-Numeric'] + "_" + df.at[item, 'Edition_Order']
        frame_id = issue_id + "_" + f'{page_num:02}'
        digital_file_name = df.at[item, 'ISSUE_NO'] + "_" + f'{page_num:04}'
        rename = "ren " + digital_file_name + ".* " + frame_id + ".*"
        item_pages = {'Title': df.at[item, 'Title'],
                      'Standard_Title': df.at[item, 'Standard_Title'],
                      'LCCN': df.at[item, 'LCCN'],
                      'Date': df.at[item, 'Date'],
                      'Date-Numeric': df.at[item, 'Date-Numeric'],
                      'Volume_Number': df.at[item, 'Volume_Number'],
                      'Issue_Number': df.at[item, 'Issue_Number'],
                      'Edition_Order': df.at[item, 'Edition_Order'],
                      'Page_Sequence_Number': page_num,
                      'Page_Physical_Description': df.at[item, 'Page_Physical_Description'],
                      'Frame_ID': frame_id,
                      'Issue_ID': issue_id,
                      'Reproduction_Agency': df.at[item, 'Reproduction_Agency'],
                      'Reproduction_Agency_Code': df.at[item, 'Reproduction_Agency_Code'],
                      'Reproduction_Note': df.at[item, 'Reproduction_Note'],
                      'Physical_Location': df.at[item, 'Physical_Location'],
                      'Physical_Location_Code': df.at[item, 'Physical_Location_Code'],
                      'Batch_Name': df.at[item, 'Batch_Name'],
                      'Reel_Number': df.at[item, 'Reel_Number'],
                      'Reel_Sequence_Number': df.at[item, 'Reel_Sequence_Number'],
                      'Digital_Filename': digital_file_name,
                      'File_Rename': rename
                      }

        rows_list.append(item_pages)

# Create page level data frame
pageLevelDf = pd.DataFrame(rows_list)
pageLevelDf['Reel_Sequence_Number'] = pageLevelDf.index + 1

# Export to new Excel file
with pd.ExcelWriter(metadata_file) as writer:
    pageLevelDf.to_excel(writer, index=False)

# Export rename column to .bat file
with open(batch_file, 'w') as f:
    f.write(pageLevelDf['File_Rename'].str.cat(sep='\n'))

# Drop rename column
pageLevelDf.drop(columns="File_Rename", inplace=True)

# Export to XML
with open(xml_file, 'w') as f:
    pageLevelDf.to_xml(xml_file, index=False, root_name="root")



