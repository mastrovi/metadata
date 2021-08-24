import os, requests, csv, shutil, time, mimetypes, subprocess
import pandas as pd
import urllib.parse as urlparse
import urllib.request
import img_dl_cdm, img_dl_digitalcommons, img_dl_dspace, img_dl_generic, img_dl_omeka, img_dl_islandora

# repos and their DAMS
repo_dams = {
    'aasu' : img_dl_digitalcommons,
    'auu' : img_dl_islandora,
    'columbus' : img_dl_omeka,
    'gbc' : img_dl_omeka,
    'gcl' : img_dl_generic,
    'geh' : img_dl_cdm,
    'gkj' : img_dl_dspace,
    'gpm' : img_dl_digitalcommons,
    'gpm-hend' : img_dl_digitalcommons,
    'gsu' : img_dl_cdm,
    'fcs' : img_dl_omeka,
    'hbcula' : img_dl_cdm,
    'mercer' : img_dl_dspace,
    'valdosta' : img_dl_dspace
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

dl_file.image_downloader(input_file)