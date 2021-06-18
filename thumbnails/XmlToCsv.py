# Importing the required libraries
import os, re
import xml.etree.ElementTree as ET
import pandas as pd

class modifications(object):
    '''
    Dynamically calls the function required to do thumbnail url pattern replacements based on:
        record_id repo prefix, edm_is_shown_at

    def [repo]_replace():
        Does appropriate replacements
        Returns:
            urls (as tuple) for csv

    def repoWork():
        Call the approriate replace function based on repo code
        Args:
            repo, edm_is_shown_at
        Returns:
            urls provided but the [repo]_replace function
    '''
    def __init__(self, repo, edm_is_shown_at):
        self.repo = repo
        self.edm_is_shown_at = edm_is_shown_at

    def auu_replace(self):
        url2 = re.sub('http(.*):(.*):(.*)', r'http\1:\2%3A\3', self.edm_is_shown_at)
        url_rpl1 = self.edm_is_shown_at + "/datastream/TN/view"
        url_rpl2 = url_rpl1.replace('http://hdl.handle.net/20.500.12322/', 'https://radar.auctr.edu/islandora/object/')
        url = re.sub('http(.*):(.*):(.*)', r'http\1:\2%3A\3', url_rpl2)
        return (url, url2)

    def columbus_replace(self):
        url = self.edm_is_shown_at
        url2 = self.edm_is_shown_at
        return (url, url2)

    def geh_replace(self):
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://album.atlantahistorycenter.com/cdm/ref/collection/', 'https://album.atlantahistorycenter.com/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://album.atlantahistorycenter.com/cdm/ref/', 'https://album.atlantahistorycenter.com/digital/')
        return (url, url2)

    def gkj_replace(self):
        url_repl1 = edm_is_shown_at.replace("https://hdl.handle.net/", "https://soar.kennesaw.edu/")
        url = url_repl1.replace("http://hdl.handle.net/", "https://soar.kennesaw.edu/")
        url2 = self.edm_is_shown_at
        return (url, url2)

    def gpm_replace(self):
        url = self.edm_is_shown_at + "/preview.jpg"
        url2 = self.edm_is_shown_at
        return (url, url2)

    def hbcula_replace(self):
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://hbcudigitallibrary.auctr.edu/cdm/ref/collection/', 'https://hbcudigitallibrary.auctr.edu/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://hbcudigitallibrary.auctr.edu/cdm/ref/', 'https://hbcudigitallibrary.auctr.edu/digital/')
        return (url, url2)

    def valdosta_replace(self):
        url_repl1 = edm_is_shown_at.replace("https://hdl.handle.net/", "https://vtext.valdosta.edu/xmlui/handle/")
        url = url_repl1.replace("http://hdl.handle.net/", "https://vtext.valdosta.edu/xmlui/handle/")
        url2 = self.edm_is_shown_at
        return (url, url2)

    def repoWork(self):
        fn = getattr(self, repo + '_replace', None)  # find method that located within the class
        if fn is not None:
            urls = fn()
            return urls


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
        repo = coll.split('_')[0]
        record_id = coll + "_" + slug

        mods = modifications(repo, edm_is_shown_at)
        urls = mods.repoWork()

        rows.append({"record_id": record_id,
                     "url": urls[0],
                     "url2": urls[1]
                     })

    df = pd.DataFrame(rows, columns=col_names)

    # Writing dataframe to csv without row numbers
    df.to_csv(file_name, index=False)
