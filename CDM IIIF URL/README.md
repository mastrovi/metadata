As of 2022-07-26, OCLC has only implemented IIIF manifests for image files (jpg, png, etc.). PDF manifests have not yet been implemented. Use facets to isolate the appropriate records (non-Moving image, non-Sound, non-PDF files). Make sure that the format of the base url is consistent accross the records.


This perl program adds IIIF urls to ContentDM records that already exist in DLGADMIN.

1. Place this script and the file you want to update into the same folder.
2. Run the program. Enter the name of the XML file you want to update.
3. Enter the base URL for the ContentDM site. Be sure to include https: and the base url should not end with a / .
4. The updated XML file will be created in the same folder and is the original file name with -iiif appended.
5. Do the following searches to make sure that there are no empty or misformed IIIF URL values and update as necessary.
    a. iiif/2/:
    b. \<iiif_partner_url\>\r\n\</iiif_partner_url\>
