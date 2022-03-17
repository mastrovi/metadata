from sickle import Sickle

# -- Set harvest URL

sickle = Sickle('https://libraries.mercer.edu/ursa/oai/request')

# -- Get MetadataFormats

formats = sickle.ListMetadataFormats()

for forms in formats:
    print(forms)

# -- Create record file(s)

f = open('sets.xml', 'w+')

# -- Print xml declaration and opening tag

print("<?xml version='1.0' encoding='UTF-8'?>", file=f)

print("<records>", file=f)

# -- Get Sets

sets = sickle.ListSets()

for s in sets:
    print(s, file=f)

# -- Print closing tag

print("</records>", file=f)

f.close()

# -- Create record file(s)

f = open('harvest.xml', 'w+')

# -- Print xml declaration and opening tag

print("<?xml version='1.0' encoding='UTF-8'?>", file=f)

print("<records>", file=f)

# -- Set metadata prefix and set

records = sickle.ListRecords(
    **{'metadataPrefix': 'oai_dc',
       'from': '1999-01-01',
       'set': 'com_10898_649',
       'ignore_deleted': 'True'
       })

for rec in records:
    print(rec, file=f)

# -- Print closing tag

print("</records>", file=f)

f.close()
