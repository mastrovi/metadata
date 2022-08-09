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
        Call the appropriate replace function based on repo code
        Args:
            repo, edm_is_shown_at
        Returns:
            urls provided but the [repo]_replace function
    '''
    def __init__(self, repo, edm_is_shown_at):
        self.repo = repo
        self.edm_is_shown_at = edm_is_shown_at
        
    def aaa_replace(self):
        # Reformatted urls should look like:
        # url = http://content.lib.auburn.edu/digital/iiif/aunumphoto/32/full/300,/0/default.jpg
        # url2 = https://content.lib.auburn.edu/digital/collection/aunumphoto/id/32/
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://content.lib.auburn.edu/cdm/ref/collection/', 'http://content.lib.auburn.edu/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://content.lib.auburn.edu/cdm/ref/', 'http://content.lib.auburn.edu/digital/')
        return (url, url2)    

    def aar_replace(self):
        # Reformatted urls should look like:
        # url = http://digital.archives.alabama.gov/digital/iiif/photo/1548/full/300,/0/default.jpg
        # url2 = http://digital.archives.alabama.gov/digital/collection/photo/id/1548
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://digital.archives.alabama.gov/cdm/ref/collection/', 'http://digital.archives.alabama.gov/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://digital.archives.alabama.gov/cdm/ref/', 'http://digital.archives.alabama.gov/digital/')
        return (url, url2)

    def aasu_replace(self):
        # Only first url modified, urls should look like:
        # url = https://digitalcommons.georgiasouthern.edu/art-savannah-lane/1/preview.jpg
        # url2 = https://digitalcommons.georgiasouthern.edu/art-savannah-lane/1
        url = self.edm_is_shown_at + "/preview.jpg"
        url2 = self.edm_is_shown_at
        return (url, url2)

    def abj_replace(self):
        # Reformatted urls should look like:
        # url = http://cdm16044.contentdm.oclc.org/digital/iiif/BPLSB02/100/full/300,/0/default.jpg
        # url2 = http://cdm16044.contentdm.oclc.org/digital/collection/BPLSB02/id/100
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://cdm16044.contentdm.oclc.org/cdm/ref/collection/', 'http://cdm16044.contentdm.oclc.org/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://cdm16044.contentdm.oclc.org/cdm/ref/', 'http://cdm16044.contentdm.oclc.org/digital/')
        return (url, url2)
    
    def alm_replace(self):
        # Only first url modified, urls should look like:
        # url = https://digitalcollections.libraries.ua.edu/utils/getthumbnail/collection/u0001_2008003/id/1
        # url2 = https://digitalcollections.libraries.ua.edu/digital/collection/u0001_2008003/id/1
        url = self.edm_is_shown_at.replace('https://digitalcollections.libraries.ua.edu/digital/', 'https://digitalcollections.libraries.ua.edu/utils/getthumbnail/')
        url2 = self.edm_is_shown_at
        return (url, url2)

    def auu_replace(self):
        # Reformatted urls should look like:
        # url = https://radar.auctr.edu/islandora/object/auc.101%3A0014/datastream/TN/view
        # url2 = http://hdl.handle.net/20.500.12322/auc.101%3A0014
        url2 = re.sub('http(.*):(.*):(.*)', r'http\1:\2%3A\3', self.edm_is_shown_at)
        url_rpl1 = self.edm_is_shown_at + "/datastream/TN/view"
        url_rpl2 = url_rpl1.replace('http://hdl.handle.net/20.500.12322/', 'https://radar.auctr.edu/islandora/object/')
        url = re.sub('http(.*):(.*):(.*)', r'http\1:\2%3A\3', url_rpl2)
        return (url, url2)

    def carter_replace(self):
        # No reformatting, just putting urls into the correct csv format
        url = self.edm_is_shown_at
        url2 = self.edm_is_shown_at
        return (url, url2)

    def columbus_replace(self):
        # No reformatting, just putting urls into the correct csv format
        url = self.edm_is_shown_at
        url2 = self.edm_is_shown_at
        return (url, url2)

    def dhs_replace(self):
        # No reformatting, just putting urls into the correct csv format
        url = self.edm_is_shown_at
        url2 = self.edm_is_shown_at
        return (url, url2)

    def dlg_replace(self):
        # Reformatted urls should look like:
        # url = https://dlg.usg.edu/record/dlg_sanb_abbeville-1899#item/full/300,/0/default.jpg
        # url2 = https://dlg.usg.edu/record/dlg_sanb_abbeville-1899#item
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url = re.sub('/record/(.*)_(.*)_(.*)#item', r'/images/iiif/2/dlg%2F\1%2F\2%2F\1_\2_\3%2F\1_\2_\3-00001.jp2', url_rpl1)
        url2 = self.edm_is_shown_at
        return (url, url2)

    def fcs_replace(self):
        # No reformatting, just putting urls into the correct csv format
        url = self.edm_is_shown_at
        url2 = self.edm_is_shown_at
        return (url, url2)
    
    def fqr_replace(self):
        # Reformatted urls should look like:
        # url =
        # url2 =
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://digitalcollections.library.miami.edu/cdm/ref/collection/', 'https://digitalcollections.library.miami.edu/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://digitalcollections.library.miami.edu/cdm/ref/', 'https://digitalcollections.library.miami.edu/digital/')
        return (url, url2)
    
    def gbc_replace(self):
        # No reformatting, just putting urls into the correct csv format
        url = self.edm_is_shown_at
        url2 = self.edm_is_shown_at
        return (url, url2)

    def gcl_replace(self):
        # Reformatted urls should look like:
        # url =
        # url2 =
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://cdm17323.contentdm.oclc.org/cdm/ref/collection/', 'https://cdm17323.contentdm.oclc.org/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://cdm17323.contentdm.oclc.org/cdm/ref/', 'https://cdm17323.contentdm.oclc.org/digital/')
        return (url, url2)

    def geh_replace(self):
        # Reformatted urls should look like:
        # url =
        # url2 =
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://album.atlantahistorycenter.com/cdm/ref/collection/', 'https://album.atlantahistorycenter.com/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://album.atlantahistorycenter.com/cdm/ref/', 'https://album.atlantahistorycenter.com/digital/')
        return (url, url2)

    def geusc_replace(self):
        # Only first url modified, urls should look like:
        # https://curate.library.emory.edu//iiif/088qbzkh6r-cor/thumbnail
        #url =
        #url2 =
        return (url, url2)

    def gkj_replace(self):
        # Reformatted urls should look like:
        # url =
        # url2 =
        url_repl1 = self.edm_is_shown_at.replace("https://hdl.handle.net/", "https://soar.kennesaw.edu/")
        url = url_repl1.replace("http://hdl.handle.net/", "https://soar.kennesaw.edu/")
        url2_repl1 = self.edm_is_shown_at.replace("https://hdl.handle.net/", "https://soar.kennesaw.edu/")
        url2 = url2_repl1.replace("http://hdl.handle.net/", "https://soar.kennesaw.edu/")
        return (url, url2)

    def gnd_replace(self):
        # Only first url modified, urls should look like:
        # url = http://digitalcommons.northgeorgia.edu/corps_photos/1/preview.jpg
        # url2 = http://digitalcommons.northgeorgia.edu/corps_photos/1
        url = self.edm_is_shown_at + "/preview.jpg"
        url2 = self.edm_is_shown_at
        return (url, url2)

    def gpm_replace(self):
        # Only first url modified, urls should look like:
        # url = https://digitalcommons.georgiasouthern.edu/art-savannah-lane/1/preview.jpg
        # url2 = https://digitalcommons.georgiasouthern.edu/art-savannah-lane/1
        url = self.edm_is_shown_at + "/preview.jpg"
        url2 = self.edm_is_shown_at
        return (url, url2)

    def gpmhend_replace(self):
        # Only first url modified, urls should look like:
        # url = https://digitalcommons.georgiasouthern.edu/george-anne/2425/preview.jpg
        # url2 = https://digitalcommons.georgiasouthern.edu/george-anne/2425
        url = self.edm_is_shown_at + "/preview.jpg"
        url2 = self.edm_is_shown_at
        return (url, url2)

    def gsu_replace(self):
        # Reformatted urls should look like:
        # url = http://digitalcollections.library.gsu.edu/digital/iiif/gawl/511/full/300,/0/default.jpg
        # url2 = http://digitalcollections.library.gsu.edu/digital/collection/gawl/id/511
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://digitalcollections.library.gsu.edu/cdm/ref/collection/', 'http://digitalcollections.library.gsu.edu/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://digitalcollections.library.gsu.edu/cdm/ref/', 'http://digitalcollections.library.gsu.edu/digital/')
        return (url, url2)

    def hbcula_replace(self):
        # Reformatted urls should look like:
        # url = https://hbcudigitallibrary.auctr.edu/digital/iiif/nccu/0/full/300,/0/default.jpg
        # url2 = https://hbcudigitallibrary.auctr.edu/digital/collection/nccu/id/0
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://hbcudigitallibrary.auctr.edu/cdm/ref/collection/', 'https://hbcudigitallibrary.auctr.edu/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://hbcudigitallibrary.auctr.edu/cdm/ref/', 'https://hbcudigitallibrary.auctr.edu/digital/')
        return (url, url2)

    def int_replace(self):
        # Only first url modified, urls should look like:
        # url = https://texashistory.unt.edu/ark:/67531/metapth836709/small/
        # url2 = https://texashistory.unt.edu/ark:/67531/metapth836709/
        url = self.edm_is_shown_at + "small/"
        url2 = self.edm_is_shown_at
        return (url, url2)

    def lru_replace(self):
        # Only first url modified, urls should look like:
        # url = https://texashistory.unt.edu/ark:/67531/metapth836709/small/
        # url2 = https://texashistory.unt.edu/ark:/67531/metapth836709/
        url = self.edm_is_shown_at + "/datastream/TN/view"
        url2 = self.edm_is_shown_at
        return (url, url2)

    def mercer_replace(self):
        url_repl1 = self.edm_is_shown_at.replace("https://hdl.handle.net/", "https://ursa.mercer.edu/")
        url_repl2 = url_repl1.replace("http://hdl.handle.net/", "https://ursa.mercer.edu/")
        url = url_repl2.replace("https://libraries.mercer.edu/ursa/", "https://ursa.mercer.edu/")
        url2_repl1 = self.edm_is_shown_at.replace("https://hdl.handle.net/", "https://ursa.mercer.edu/")
        url2_repl2 = url2_repl1.replace("https://libraries.mercer.edu/ursa/", "https://ursa.mercer.edu/")
        url2 = url2_repl2.replace("http://hdl.handle.net/", "https://ursa.mercer.edu/")
        return (url, url2)

    def mum_replace(self):
        # No reformatting, just putting urls into the correct csv format
        url = self.edm_is_shown_at
        url2 = self.edm_is_shown_at
        return (url, url2)

    def nge_replace(self):
        # No reformatting, just putting urls into the correct csv format
        url = self.edm_is_shown_at
        url2 = self.edm_is_shown_at
        return (url, url2)
    
    def src_replace(self):
        # Only first url modified, urls should look like:
        # url = https://localhistory.richlandlibrary.com/digital/iiif/p16817coll21/324/full/300,/0/default.jpg
        # url2 = https://localhistory.richlandlibrary.com/digital/collection/p16817coll21/id/324
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('https://localhistory.richlandlibrary.com/digital/collection/', 'https://localhistory.richlandlibrary.com/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at
        return (url, url2)

    def suc_replace(self):
        # Reformatted urls should look like:
        # url = https://digital.tcl.sc.edu/digital/iiif/adamsea/12/full/300,/0/default.jpg
        # url2 = https://digital.tcl.sc.edu/digital/collection/adamsea/id/12
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('https://digital.tcl.sc.edu/digital/collection/', 'https://digital.tcl.sc.edu/digital/iiif/')
        url_rpl3 = url_rpl2.replace('http://cdm17173.contentdm.oclc.org/cdm/ref/collection/', 'https://digital.tcl.sc.edu/digital/iiif/')
        url_rpl4 = url_rpl3.replace('http://digital.tcl.sc.edu/cdm/ref/collection/', 'https://digital.tcl.sc.edu/digital/iiif/')
        url = url_rpl4.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://digital.tcl.sc.edu/cdm/ref/collection/', 'http://digital.tcl.sc.edu/digital/')
        return (url, url2)

    def tws_replace(self):
        # Reformatted urls should look like:
        # url = http://dlynx.rhodes.edu:8080/jspui/handle/10267/34243
        # url2 = http://dlynx.rhodes.edu:8080/jspui/handle/10267/34243
        url_repl1 = edm_is_shown_at.replace("https://hdl.handle.net/", "http://dlynx.rhodes.edu:8080/jspui/handle/")
        url = url_repl1.replace("http://hdl.handle.net/", "http://dlynx.rhodes.edu:8080/jspui/handle/")
        url2_repl1 = edm_is_shown_at.replace("https://hdl.handle.net/", "http://dlynx.rhodes.edu:8080/jspui/handle/")
        url2 = url2_repl1.replace("http://hdl.handle.net/", "http://dlynx.rhodes.edu:8080/jspui/handle/")
        return (url, url2)

    def ugalaw_replace(self):
        # No reformatting, just putting urls into the correct csv format
         url = self.edm_is_shown_at
         url2 = self.edm_is_shown_at
         return (url, url2)

    def usm_replace(self):
        # Only first url modified, urls should look like:
        # url = https://usm.access.preservica.com/download/thumbnail/IO_3a6951e4-7eff-46df-b8a6-d683d15957d9
        # url2 = https://usm.access.preservica.com/uncategorized/IO_3a6951e4-7eff-46df-b8a6-d683d15957d9
        url = self.edm_is_shown_at.replace("https://usm.access.preservica.com/uncategorized/", "https://usm.access.preservica.com/download/thumbnail/")
        url2 = self.edm_is_shown_at
        return (url, url2)

    def valdosta_replace(self):
        url_repl1 = edm_is_shown_at.replace("https://hdl.handle.net/", "https://vtext.valdosta.edu/xmlui/handle/")
        url = url_repl1.replace("http://hdl.handle.net/", "https://vtext.valdosta.edu/xmlui/handle/")
        url2_repl1 = edm_is_shown_at.replace("https://hdl.handle.net/", "https://vtext.valdosta.edu/xmlui/handle/")
        url2 = url2_repl1.replace("http://hdl.handle.net/", "https://vtext.valdosta.edu/xmlui/handle/")
        return (url, url2)

    def vrc_replace(self):
        # Only first url modified, urls should look like:
        # url = https://digital.library.vcu.edu/islandora/object/vcu%3A36117/datastream/TN/view
        # url2 = https://digital.library.vcu.edu/islandora/object/vcu%3A36117
        url = self.edm_is_shown_at + "/datastream/TN/view"
        url2 = self.edm_is_shown_at
        return (url, url2)
    
    def xhs_replace(self):
        # Reformatted urls should look like:
        # url = http://images.indianahistory.org/digital/iiif/BPLSB02/100/full/300,/0/default.jpg
        # url2 = http://images.indianahistory.org/digital/collection/BPLSB02/id/100
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://images.indianahistory.org/cdm/ref/collection/', 'http://images.indianahistory.org/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://images.indianahistory.org/cdm/ref/', 'http://images.indianahistory.org/digital/')
        return (url, url2)
    
    def wsh_replace(self):
        # Reformatted urls should look like:
        # url = http://content.wisconsinhistory.org/digital/iiif/BPLSB02/100/full/300,/0/default.jpg
        # url2 = http://content.wisconsinhistory.org/digital/collection/BPLSB02/id/100
        url_rpl1 = self.edm_is_shown_at + "/full/300,/0/default.jpg"
        url_rpl2 = url_rpl1.replace('http://content.wisconsinhistory.org/cdm/ref/collection/', 'http://content.wisconsinhistory.org/digital/iiif/')
        url = url_rpl2.replace('/id', '')
        url2 = self.edm_is_shown_at.replace('http://content.wisconsinhistory.org/cdm/ref/', 'http://content.wisconsinhistory.org/digital/')
        return (url, url2)

    def youtube_replace(self):
        # Only first url modified, urls should look like:
        # url = http://img.youtube.com/vi/MEXWrrRMT6A/hqdefault.jpg
        # url2 = https://www.youtube.com/embed/MEXWrrRMT6A
        url1 = self.edm_is_shown_at.replace("https://www.youtube.com/embed/","http://img.youtube.com/vi/")
        url2 = url1.replace("https://youtube.com/embed/", "http://img.youtube.com/vi/")
        url = url2 + "/hqdefault.jpg"
        url2 = self.edm_is_shown_at
        return (url, url2)

    def repoWork(self):
        # find method that located within the class
        fn = getattr(self, repo + '_replace', None)
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
        try:
            edm_is_shown_by = item.find("edm_is_shown_by/edm_is_shown_by").text
        except:
            edm_is_shown_by = "none"
        try:
            iiif_partner_url = item.find("iiif_partner_url").text
        except:
            iiif_partner_url = "none"
        repo = coll.split('_')[0]
        if "-" in repo:
            repo = repo.replace("-","")
        record_id = coll + "_" + slug

        if "youtube" in edm_is_shown_by:
            repo = "youtube"
            mods = modifications(repo, edm_is_shown_by)
            urls = mods.repoWork()
        elif "#item" in edm_is_shown_by:
            repo = "dlg"
            mods = modifications(repo, edm_is_shown_by)
            urls = mods.repoWork()
        elif "geusc" in repo or "emt" in repo or "emo" in repo:
            repo = "geusc"
            mods = modifications(repo, iiif_partner_url)
            urls = mods.repoWork()

        else:
            mods = modifications(repo, edm_is_shown_at)
            urls = mods.repoWork()

        rows.append({"record_id": record_id,
                     "url": urls[0],
                     "url2": urls[1]
                     })

    df = pd.DataFrame(rows, columns=col_names)

    # Writing dataframe to csv without row numbers
    df.to_csv(file_name, index=False)
