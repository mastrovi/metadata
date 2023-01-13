import pandas as pd
import img_dl_cdm, img_dl_digitalcommons, img_dl_dspace, img_dl_generic, img_dl_iiif_manifest, img_dl_omeka, img_dl_islandora, img_dl_wp

# repos and their DAMS
repo_dams = {
    'aar' : img_dl_cdm,
    'aasu' : img_dl_digitalcommons,
    'abj' : img_dl_cdm,
    'alm' : img_dl_cdm,
    'auu' : img_dl_islandora,
    'bcri' : img_dl_generic,
    'carter' : img_dl_generic,
    'columbus' : img_dl_omeka,
    'csu' : img_dl_cdm,
    'dhs' : img_dl_omeka,
    'emo' : img_dl_iiif_manifest,
    'emt' : img_dl_iiif_manifest,
    'gbc' : img_dl_omeka,
    'gcl' : img_dl_cdm,
    'geh' : img_dl_cdm,
    'geusc' : img_dl_iiif_manifest,
    'gkj' : img_dl_dspace,
    'gnd' : img_dl_digitalcommons,
    'gpm' : img_dl_digitalcommons,
    'gpm-hend' : img_dl_digitalcommons,
    'gsu' : img_dl_cdm,
    'fcs' : img_dl_omeka,
    'fqr' : img_dl_cdm,
    'hbcula' : img_dl_cdm,
    'int' : img_dl_generic,
    'lru' : img_dl_islandora,
    'mercer' : img_dl_dspace,
    'mum' : img_dl_digitalcommons,
    'nge' : img_dl_wp,
    'suc' : img_dl_cdm,
    'tws' : img_dl_dspace,
    'ugalaw' : img_dl_digitalcommons,
    'usm' : img_dl_generic,
    'valdosta' : img_dl_dspace,
    'vrc' : img_dl_islandora
}

# Ask for file
input_file = input("Input the collectionSlug.csv with two values: record_id,url: ")
input_file = input_file.strip('\"')

# get repo
df = pd.read_csv(input_file)
row_two = df.iloc[0]
repo = row_two[0]
repo_code = repo.split('_')[0]
dl_file = repo_dams[repo_code]

# Run approriate respository script
dl_file.image_downloader(input_file)