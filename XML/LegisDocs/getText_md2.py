import os, htmltabletomd
from bs4 import BeautifulSoup
from lxml import etree as ET

def collapse_tags(element, value):
    # Element = the lxml element, value = the top level tag that needs children tags collapsed
    context = ET.iterwalk(element, events=('end',))
    index = 0
    for event, elem in context:
        # Looking for the elements in the structure list
        if elem.tag == str(value):
            index += 1
            soup = BeautifulSoup(ET.tostring(elem), "lxml")
            collapsedText = soup.get_text()
    return collapsedText

def law_container(lawTag, volume="", partTitle="", lawdivTitle=""):
    # Create law filename
    partLevelFile = "GA" + lawTag.attrib['id'][1:5] + "-" + lawTag.attrib['id'][6:7] + "-P" + lawTag.attrib[
        'initial.page'] + "-" + lawTag.attrib['id']
    # Find certain elements in law
    textNodes = list(lawTag)
    textNodeindex = 0
    fullExist = lawTag.find('fulltitle')

    # Insert law div heading in page
    if lawdivTitle != "":
        lawdivTitleInsert = ET.Element('lawdivTitle')
        lawdivTitleInsert.text = "#### " + lawdivTitle
        lawTag.insert(0, lawdivTitleInsert)

    # Insert lawdiv Title heading in page
    if partTitle != "":
        partTitleInsert = ET.Element('lawdivPart')
        partTitleInsert.text = "#### " + partTitle
        lawTag.insert(0, partTitleInsert)

    # Insert volume heading in page
    volumeInsert = ET.Element('volume')
    volumeInsert.text = "#### " + volume
    lawTag.insert(0, volumeInsert)

    for node in textNodes:
        if node.tag == "lawtype":
            node.text = "#### Law Type: " + str(node.text)
            textNodeindex += 1
        elif node.tag == "shorttitle":
            node.text = "#### Short Title: " + str(node.text)
            # If no full title
            if fullExist is None:
                titleHeading = node.text
                titleHeading = titleHeading.replace("#### Short Title: ", "")
                titleHeading = "# " + titleHeading.replace('**', '').replace('\n', '')
                # Insert law title as page title heading
                titleInsert = ET.Element('titleheading')
                titleInsert.text = titleHeading
                lawTag.insert(0, titleInsert)
                textNodeindex += 1
            textNodeindex += 1
        elif node.tag == "origin":
            node.text = "#### Origin: " + str(node.text)
            textNodeindex += 1
        elif node.tag == "lawnbr":
            node.text = "#### Law Number: " + str(node.text)
            textNodeindex += 1
        elif node.tag == "fulltitle":
            fulltitle = node.text
            fulltitle = fulltitle.replace('-------',"")
            # Fix some wonky formatting
            if fulltitle.startswith('\n'):
                fulltitle = fulltitle.lstrip('\n')
            if '\n' in fulltitle:
                fulltitle = fulltitle.replace('\n', ' ')
            titleHeading = node.text
            titleHeading = "# " + titleHeading.replace('**', '').replace('\n', '').replace('-------',"")
            node.text = "**Full Title:** " + str(fulltitle)
            # Insert law title as page title heading
            titleInsert = ET.Element('titleheading')
            titleInsert.text = titleHeading
            lawTag.insert(0, titleInsert)
            textNodeindex += 1
        elif node.tag == "approvaldate":
            node.text = "#### Approval Date: " + str(node.text)
            textNodeindex += 1
        else:
            textNodeindex += 1
    split_to_text(lawTag, lawTag.tag, partLevelFile)

def lawdiv_container(lawdivTag, volumeText, partTitle=""):
    # Find certain elements in law
    textNodes = list(lawdivTag)
    textNodeindex = 0
    lawdivTitle = ""
    #contents =

    for node in textNodes:
        if node.tag == "title":
            fulltitle = collapse_tags(node, node.tag)
            if fulltitle.startswith('\n'):
                fulltitle = fulltitle.lstrip('\n')
            if '\n' in fulltitle:
                fulltitle = fulltitle.replace('\n', ' ')
            lawdivTitle = fulltitle
            titleHeading = fulltitle
            titleHeading = "# " + titleHeading
            node.text = "**Title:** " + str(fulltitle)
            # Insert law title as page title heading
            titleInsert = ET.Element('titleheading')
            titleInsert.text = titleHeading
            lawdivTag.insert(0, titleInsert)
            textNodeindex += 1
        # Add to contents list file
        # elif node.tag == 'law':
        #     law_container(node, volumeText, partTitle, lawdivTitle)
        # Do the law tag processing
        elif node.tag == 'law':
            law_container(node, volumeText, partTitle, lawdivTitle)

def replacements(text):
    # replaces characters to make filename DLG friendly
    newText = text.replace(".", "-")
    newText2 = newText.replace("(","")
    newText3 = newText2.replace(")", "")
    return newText3

def split_to_text(element, value, fileName):
    # This does the XML splitting work
    context = ET.iterwalk(element, events=('end',))
    index = 0
    # Add .md file extention
    fileName2 = replacements(fileName)
    fileNameEXT =  fileName2 + ".md"
    # Open file and do work
    with open(fileNameEXT, 'w') as f:
        # Get the rest of the page content
        for event, elem in context:
            # Looking for the elements in the structure list
            if elem.tag == str(value):
                index += 1
                # Get the chunks of xml
                soup = BeautifulSoup(ET.tostring(elem), "lxml")
                # Try to markdown format any table in this chunk of elements
                elementTables = soup.find_all("table")
                tableIndex = 0
                if len(elementTables) > 0:
                    for table in elementTables:
                        table = elementTables[tableIndex].prettify()
                        # Create new table
                        newTag = soup.new_tag("newTable")
                        md_table = htmltabletomd.convert_table(table)
                        md_table = md_table.replace('<br>', ' ')
                        newTag.append(md_table)
                        try:
                            # Try to add the element right after the original table (like in law div)
                            elementTables[tableIndex].insert_after(newTag)
                        except:
                            # Just append the table because its doesn't have a parent (like in backmatter pages)
                            elementTables[tableIndex].append(newTag)
                        # Remove original unformatted table element
                        elementTables[tableIndex].extract()
                        tableIndex =+ 1
                # Add filename for easier reference
                if fileName2 != 'index':
                    filetag = soup.new_tag('filename')
                    filetag.append("File name: " +  fileName2)
                    soup.append(filetag)
                # Strip out any remaining tags
                textSoup = soup.get_text('\n', strip=True)
                textSoup = textSoup.replace('\n\n', '\n')
                lineLength = len(textSoup.splitlines())
                # Split the chunk of text into lines to write them one by one
                lines = textSoup.splitlines()
                lineCount = 0
                # Remove trailing horizontal rule
                if lineLength > 0:
                    if lines[lineLength-1] == '-------':
                        lines[lineLength-1] = ""
                for line in lines:
                    # I'm honestly not sure what this is doing but it's writing without a new line at the end
                    if line == lines[lineLength-1]:
                        f.write(line)
                        lineCount += 1
                    # Check for start of table and add preceding single new line
                    elif line.startswith('|') and not lines[lineCount-1].startswith('|'):
                        f.write("\n\n" + line + "\n")
                        lineCount += 1
                    # Check for table boundary and do single new line
                    elif line.startswith('|'):
                        f.write(line + "\n")
                        lineCount += 1
                    # Make sure pages have the right spacing:
                    elif line.startswith('Page'):
                        f.write(line + "\n\n")
                        lineCount += 1
                    # Check if the preceding line is part of a table or horizontal rule and add an extra new line to ensure proper formatting
                    elif not line.startswith('|') and (lines[lineCount-1].startswith('|') or lines[lineCount-1].startswith('-------')):
                        f.write("\n" + line)
                        lineCount += 1
                    # Do a double new line (markdown paragraph)
                    else:
                        f.write(line + "\n\n")
                        lineCount += 1
        if fileNameEXT == 'index.md':
            f.write("\n\n## Contents:\n")
    # Generate a TOC for each directory
    # If not the index file read the first line of the newly created file and add it to the index
    if fileNameEXT != 'index.md':
        with open(fileNameEXT, 'r') as f, open('index.md', 'a') as w:
            firstline = f.readline()
            newLine = "\n- [" + firstline.replace('\n','').replace('*','').replace('# ','').replace('#','') + "](" + fileNameEXT + ")"
            w.write(newLine)

def toc_container(lawTag, volume="", partTitle=""):
    # Insert volume heading in page
    volumeInsert = ET.Element('volume')
    volumeInsert.text = "#### " + volume
    lawTag.insert(0, volumeInsert)

def unwrap_text(elementText):
    # strips out tags inside
    soup = BeautifulSoup(ET.tostring(elementText), "lxml")
    textSoup = soup.get_text(' ', strip=True)
    return textSoup

# Insert directory path here
path = ""

# Change to path directory
os.chdir(path)

# Find files
files = [fi for fi in os.listdir(path) if fi.endswith('_md.xml')]

# set up various year tracking
allYears = []
multiYear = []
multiYearHeadingList = []

# Find years with more than one volume
for f in files:
    # Gets filename without extension
    base = os.path.splitext(f)[0]
    year = base[0:4]
    if year not in allYears:
        allYears.append(year)
    else:
        multiYear.append(year)

# For each file
for f in files:
    # Gets filename without extension
    base = os.path.splitext(f)[0]
    year = base[0:4]
    month = base[4:6]
    # Appends filename to directory path
    yearDir = str(path) + '\\' + year
    yearMonthDir = yearDir + '\\' + year + "-" + month
    # Creates year directory
    if not os.path.exists(yearDir):
        # if directory Doesnt Exist Create it.
        os.makedirs(yearDir)

    # parse xml and establish the various upper level trees
    tree = ET.parse(f)
    root = tree.getroot()
    metadata = root[0]
    document = root[1]
    body = root.find('document/body')

    # Change to year directory
    os.chdir(yearDir)

    # Status print to console
    print("Working on " + year + "-" + month)

    # Declare index.md name
    indexMD = "index"

    # Produce and save metadata in directory index file
    # Get the tags and text of the direct children
    metaIndex = 0
    metaTag = list(metadata)
    for tag in metaTag:
        # Rename coretitle
        if metaTag[metaIndex].tag == 'coretitle':
            metaTag[metaIndex].tag = 'title'
            metaTag[metaIndex].text = '# ' + metaTag[metaIndex].text
        # Fix dates
        if metaTag[metaIndex].tag == 'date':
            readableYear = metaTag[metaIndex].text[0:4]
            if metaTag[metaIndex].text[4:6] == '00':
                metaTag[metaIndex].text = readableYear
            else:
                readableMonth = metaTag[metaIndex].text[4:6]
                metaTag[metaIndex].text = readableYear + "-" + readableMonth
        # Insert tag name into text
        if metaTag[metaIndex].text is not None and metaTag[metaIndex].tag != 'title':
            metaTag[metaIndex].text = str.capitalize(metaTag[metaIndex].tag) + ": " + metaTag[metaIndex].text
        metaIndex += 1

    # Check if multiple volumes and switch to volume directory if yes
    if year in multiYear:
        mainIndex = yearDir + '\\index.md'
        # Check if the top level index file exists and create it if not
        try:
            main = open(mainIndex)
            main.close()
        except:
            with open(mainIndex, 'w') as main:
                header = "# " + year + " Contents\n\n\n## Contents:\n"
                main.write(header)
        # Creates year directory
        if not os.path.exists(yearMonthDir):
            # if directory Doesnt Exist Create it.
            os.makedirs(yearMonthDir)
        os.chdir(yearMonthDir)

    # Clean the year index file to start from scratch
    with open("index.md", "w") as newFile:
        newFile.write("")

    # Add metadata to index file for directory
    split_to_text(metadata, "metadata", indexMD)
    # -- End metadata work --

    # Add page text to all page elements
    for page in root.xpath('//page'):
        try:
            pageNo = page.attrib["no"].rsplit(".")
            page.text = "Page " + pageNo[2] + "\n"
        except:
            page.text = "Page \[missing page number\]"

    # -- Document work --
    docEls = list(document)

    # Title page work
    titleHeading = document.find('titlepage/title')
    titleHeading = unwrap_text(titleHeading)
    titleHeading = "# " + titleHeading.replace('**','').replace('\n','')
    volumeText = titleHeading.replace("# ", "")
    sessionDates = document.findall('titlepage/sessiondate')

    # Add the title heading and link to the main index file
    if year in multiYear:
        with open(mainIndex, 'a') as w:
            newLine = "\n- [" + titleHeading.replace('# ', '') + "](" + year + "-" + month + "/index.md)"
            w.write(newLine)

    for sDate in sessionDates:
        if sDate.text[4:6] == '00':
            newDate = sDate.text[0:4]
        elif sDate.text[6:8] == '00':
            newDate = sDate.text[0:4] + "-" + sDate.text[4:6]
        else:
            newDate = sDate.text[0:4] + "-" + sDate.text[4:6]  + "-" + sDate.text[6:8]
        sDate.text = newDate
    # Append page id attribute to next tag
    for docEl in docEls:
        if docEl.tag == 'page':
            pageId = docEl.attrib['id']
        else:
            docEl.set("pageid", pageId)
            docLevelFile = docEl.attrib['pageid'] + "-" + docEl.tag
            if docEl.tag != 'body':
                # Add title page header
                if docEl.tag == 'titlepage':
                    # Insert title page heading
                    titleInsert = ET.Element('titleheading')
                    titleInsert.text = titleHeading
                    docEl.insert(0, titleInsert)
                    split_to_text(docEl, docEl.tag, docLevelFile)
                else:
                    # Insert volume in page
                    # volumeInsert = ET.Element('volume')
                    # volumeInsert.text = volumeText
                    # docEl.insert(0, volumeInsert)

                    # Create title element


                    split_to_text(docEl, docEl.tag, docLevelFile)
    # -- End document work --
    #
    # -- Body work --
    bodyEls = list(body)
    bodyPage = body.attrib['pageid']
    for bodyEl in bodyEls:
        if bodyEl.tag == 'page':
            pageId = bodyEl.attrib['id']
        else:
            for index, item in enumerate(bodyEls):
                # Set first page id
                if not index:
                    firstPartPageId = body.find('part')
                    firstPartPageId.set("pageid", bodyPage)
                # Set the rest
                else:
                    bodyEl.set("pageid", pageId)
                    bodyLevelFile = bodyEl.attrib['pageid'] + "-" + bodyEl.tag
    # -- End Body work --

    # -- Part work --
    # Find each part and get the first level of elements
    for part in bodyEls:
        partEls = list(part)
        try:
            partPageId = part.attrib['pageid']
        except:
            partPageId = part.attrib['id']
        # -- Element work --
        for partEl in partEls:
            partElChildren = list(partEl)
            partElChildrenIndex = 0
            # Assign pageid attribute
            if partEl.tag == 'page':
                partPageId = partEl.attrib['id']
            else:
                partEl.set("pageid", partPageId)
                # Do the law tag processing
                if partEl.tag == 'title':
                    partTitle = collapse_tags(partEl, partEl.tag)
                    partTitle = partTitle.replace('\n', '').replace('-------','')
                if partEl.tag == 'law':
                    law_container(partEl, volumeText)
                elif partEl.tag == 'lawdiv':
                    lawdiv_container(partEl, volumeText, partTitle)
                else:
                    partLevelFile = partEl.attrib['pageid'] + "-" + partEl.tag

                    # # Insert title page heading in page
                    # volumeInsert = ET.Element('volume')
                    # volumeInsert.text = "**Volume**: " + volumeText
                    # partEl.insert(0, volumeInsert)

                    split_to_text(partEl, partEl.tag, partLevelFile)


    # Change back to main directory
    os.chdir(path)
