#!/usr/bin/env python

import os, re

# I've been running this on the year xmls first, then getText_md2 to generate the markdown files
# --- Runs on a directory, insert path here
path = ""


# Change to path directory
os.chdir(path)

# Find files
files = [fi for fi in os.listdir(path) if fi.endswith('.xml')]

# Do work
for f in files:
    if not f.endswith('_md.xml'):
        # --- Read in the file ---
        with open(f, 'r', encoding="utf-8") as file:
            filedata = file.read()

        # --- Remove and replace basic formatting tags
        filedata = filedata.replace('<i>', '*').replace('</i>', '* ')
        filedata = filedata.replace('<b>', '**').replace('</b>', '** ')
        filedata = filedata.replace('<p>', '\n')
        filedata = filedata.replace('</p>', '')
        filedata = filedata.replace('<pre>', '').replace('</pre>', '')
        # filedata = filedata.replace('<br set=\"CENTER\">', '\n')
        # filedata = filedata.replace('<br set=\"CENTER\" />', '\n')
        # filedata = filedata.replace('</br>', '')
        # filedata = re.sub('<br .*/>', '\n', filedata)
        # filedata = filedata.replace('<br>', '\n').replace('</br>', '\n')
        #
        # --- Remove and replace lists, sidenotes, toc divisions tags
        filedata = filedata.replace('<li>', '-').replace('</li>', '')
        filedata = filedata.replace('<item>', '').replace('</item>', '')
        filedata = filedata.replace('<sidenote>', '[Sidenote: ').replace('</sidenote>', ']\n')


        # Remove indents
        filedata = filedata.replace('\t', '')

        # Remove wonky ticks
        filedata = filedata.replace('`', '\'')

        # Escape bracets
        filedata = filedata.replace('[', '\[').replace(']', '\]')

        # --- Add page horizontal lines
        filedata = re.sub('(<page .*/>)', r'------- \n \1', filedata)

        # Set up new file
        # --- Create new xml file ---
        # --- Split filename from extension
        filename = f
        (prefix, sep, suffix) = filename.rpartition('.')

        # --- Add _md to filename ---
        new_filename = prefix + '_md.xml'

        # --- Write new file --
        with open(new_filename, 'w', encoding="utf-8") as prepFile:
            prepFile.write(filedata)
            print('\n', 'Your new files have been created.')