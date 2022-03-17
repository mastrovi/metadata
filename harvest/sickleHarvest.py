from sickle import Sickle

# -- Set file save location
save_location = input("Enter the directory to save the xml: ")
file_path = save_location + '\harvest.xml'

# -- Set harvest URL
base_url = input("Enter the OAI base url: ")
sickle = Sickle(base_url)

# -- Create record file(s)
f = open(file_path, 'w+', encoding="utf-8")

# -- Print xml declaration and opening tag
print("<?xml version='1.0' encoding='UTF-8'?>", file=f)
print("<records>", file=f)

# -- Set metadata prefix and set
records = sickle.ListRecords(
           **{'metadataPrefix':'oai_qdc',
              'set':'abarr',
              'ignore_deleted':'True'
           })

for rec in records:
   print(rec, file=f)

# -- Print closing tag
print("</records>", file=f)

f.close()