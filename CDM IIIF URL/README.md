This perl program adds IIIF urls to ContentDM records that already exist in DLGADMIN.

1. Place this script and the file you want to update into the same folder.
2. Run the program. Enter the name of the XML file you want to update.
3. Enter the base URL for the ContentDM site. Be sure to include https: and the base url should not end with a / .
4. The updated XML file will be created in the same folder and is the original file name with -iiif appended.
5. Do the following searches to make sure that there are no empty or misformed IIIF URL values and update as necessary.
    a. iiif/2/:
    b. \<iiif_partner_url\>\r\n\</iiif_partner_url\>
