from sickle import Sickle

# -- Set harvest URL
sickle = Sickle('http://digitalcollections.library.gsu.edu:80/oai/oai.php')

# -- Create record file(s)
f = open('harvest.xml', 'w+', encoding="utf-8")

# -- Print xml declaration and opening tag
print("<?xml version='1.0' encoding='UTF-8'?>", file=f)
print("<records>", file=f)

# -- Set metadata prefix and set
records = sickle.ListRecords(
           **{'metadataPrefix':'oai_qdc',
           'from':'1999-01-01',
         'set':'lgbtq',
           'ignore_deleted':'True'
           })

for rec in records:
   print(rec, file=f)

# -- Print closing tag
print("</records>", file=f)

f.close()