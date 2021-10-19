#!/usr/bin/env python

import os, re, sys
from lxml import etree

# --- Ask for file, take file name with or without extension. If no extension, add it ---
# --- Uncomment for single file
#xmlFile = input('What xml file would you like to convert? (Enter full file path)')
#xmlFile = xmlFile.strip('\"')
#if ".xml" not in xmlFile:
#    xmlFile = xmlFile  + '.xml'

# --- Runs on a directory
# --- Comment out for single file
path = input('What directory would you like to run this on? ')


# Change to path directory
os.chdir(path)

# Find files
files = [fi for fi in os.listdir(path) if fi.endswith('.xml')]

# Do work
for f in files:
    # --- Read in the file ---
    with open(f, 'r', encoding="utf-8") as file:
        filedata = file.read()


    # --- Remove \r\n, tabs, and extraneous whitespace (multiple leading spaces, between brackets, etc.)
    filedata = filedata.replace('\r', '').replace('\n', '')
    filedata = filedata.replace('\t', '')
    filedata = filedata.replace('    ', '')
    filedata = filedata.replace('  ', '')
    filedata = filedata.replace('> <', '><')


    # --- Remove attributes type="integer",  nil="true",  type="boolean", type="array"
    filedata = filedata.replace(' type="integer"', '')
    filedata = filedata.replace(' nil="true"', '')
    filedata = filedata.replace(' type="boolean"', '')
    filedata = filedata.replace(' type="array"', '')


    # --- Remove specific nested tags ---
    # --- Remove <record_id> tags
    filedata = filedata.replace('<record_id>', '')
    filedata = filedata.replace('</record_id>', '')
    # --- Remove portal <code> tags
    filedata = filedata.replace('<code>', '')
    filedata = filedata.replace('</code>', '')
    filedata = filedata.replace('<portals>', '')
    filedata = filedata.replace('</portals>', '')


    # --- Replace &amp; with &amp to make splitting tags easier ---
    if filedata.find('&amp;') is not None:
        filedata = filedata.replace('&amp;', '&amp')


    # --- List of metadata fields to collapse
    fields = ['portal',
              'dc_format',
              'dc_right',
              'dc_date',
              'dc_relation',
              'dcterms_is_part_of',
              'dcterms_contributor',
              'dcterms_creator',
              'dcterms_description',
              'dcterms_extent',
              'dcterms_medium',
              'dcterms_identifier',
              'dcterms_language',
              'dcterms_spatial',
              'dcterms_publisher',
              'dcterms_rights_holder',
              'dcterms_subject',
              'dcterms_temporal',
              'dcterms_title',
              'dcterms_type',
              'edm_is_shown_at',
              'dlg_local_right',
              'dcterms_bibliographic_citation',
              'dlg_subject_personal',
              'edm_is_shown_by',
              'dcterms_provenance',
              ]

    # --- Put pipes in between multiple entries, collapse, and remove blank entries
    for field in fields:
        print ('Separating multiple ' + field + ' entries with ||')
        if filedata.find('</' + field + '><' + field + '>') is not None:
            filedata = filedata.replace('</' + field + '><' + field + '>', '||')
        print ('Removing ' + field + ' nesting')
        if filedata.find('<' + field + '><' + field + '>') is not None:
            filedata = filedata.replace('<' + field + '><' + field + '>', '<' + field + '>')
            filedata = filedata.replace('</' + field + '></' + field + '>', '</' + field + '>')
            filedata = filedata.replace('</' + field + '><' + field + '/></' + field + '>', '</' + field + '>')
        if filedata.find('<' + field + '><' + field + '/></' + field + '>') is not None:
            print ('Removing blank ' + field + ' entries')
            filedata = filedata.replace('<' + field + '><' + field + '/></' + field + '>', '<' + field + '/>')

    # --- Insert breaks so file is legible ---
    #filedata = filedata.replace('><', '>\r\n<')

    # --- Look for semicolons at the end of string (CONTENTdm specfic)
    #if filedata.find(';<') is not None:
    #    filedata = filedata.replace(';<', '<')
    #    print('Removing trailing semicolons')

    # --- Add &amp; reference back for valid XML ---
    if filedata.find('&amp') is not None:
        filedata = filedata.replace('&amp', '&#38;')

    '''Output new file with all changes'''
    # --- Create new xml file ---
    # --- Split filename from extension
    filename = f
    (prefix, sep, suffix) = filename.rpartition('.')


    # --- Add _flat to filename ---
    new_filename = prefix + '_flat.xml'


    # --- Write new file --
    with open(new_filename, 'w', encoding="utf-8") as prepFile:
      prepFile.write(filedata)

    file.close()
    prepFile.close()

    print('\n', 'Your new files have been created.')

input("Press Enter to close...")