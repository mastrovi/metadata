Files for thumbnail generation of harvested records:

1. XmlToCsv
   * Will transform ActiveXML from dlgadmin to a csv with record_id, url, url2
   * Urls are direct paths to thumbnails
   * Institution specific, prefixed with repo slug
2. Reconciliation
   * Counts the number of records from a dlg-thumbnails directory listing
3. img_dl_2.py
   * Base script without DAMS specific modifications
4. img_dl_cdm.py -- Image retrieval and download (requires XmlToCsv format)
   * Creates a folder with the same name as the csv
   * Downloads thumbnail if found and names it with record_id
   * Download full size first image or whole object, whichever is accessible
5. img_dl_digitalcommons.py -- Image retrieval and download (requires XmlToCsv format)
   * Creates a folder with the same name as the csv
   * Downloads thumbnail if found and names it with record_id
   * Download full size first image or whole object, whichever is accessible
6. img_dl_islandora.py -- Image retrieval and download (requires XmlToCsv format)
   * Creates a folder with the same name as the csv
   * Downloads thumbnail if found and names it with record_id
7. img_dl_omeka.py -- Image retrieval and download (requires XmlToCsv format)
   * Creates a folder with the same name as the csv
   * Downloads thumbnail if found and names it with record_id
   * Download full size first image or whole pdf, whichever is accessible
   * Currently, works for Columbus and FCS flavors of Omeka

   
