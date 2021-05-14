Contains two types of files for thumbnail generation of harvested records:

1. XmlToCsv.py
   * Will transform ActiveXML from dlgadmin to a csv with record_id, url, url2
   * Urls are direct paths to thumbnails
   * Institution specific
2. img_dl_cdm.py -- Image retrieval and download (requires csv format)
   * Creates a folder with the same name as the csv
   * Downloads thumbnail if found and names it with record_id
   * Download full size first image or whole pdf, whichever is accessible
3. img_dl_islandora.py -- Image retrieval and download (requires csv format)
   * Creates a folder with the same name as the csv
   * Downloads thumbnail if found and names it with record_id   

   
