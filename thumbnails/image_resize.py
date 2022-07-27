import os, re
import pypdfium2 as pdfium
from PIL import Image

path = input('What directory would you like to run this on? ')
# Change to path directory
os.chdir(path)

# Specify Max thumbnail size
MAX_SIZE = (300, 300)

# Find files for conversion
imgfiles = [fi for fi in os.listdir(path) if fi.endswith((".png", ".jpg", ".jp2"))]
pdffiles = [fi for fi in os.listdir(path) if fi.endswith('.pdf')]

if imgfiles is not None:
    # Do work on image files
    for f in imgfiles:
        # Do modifications for filename
        imgfile_rpl1 = os.path.splitext(f)[0] + ".jpg"
        imgfile_rpl2 = imgfile_rpl1.replace("full_", "")
        imgfile_rpl3 = re.sub('-\d\d\d\d\d\d', r'', imgfile_rpl2)
        imgfile_name = re.sub('-\d\d\d\d\d', r'', imgfile_rpl3)
        print("Converting ", imgfile_name)

        # Open image and create thumbnail
        image = Image.open(f)
        image.thumbnail(MAX_SIZE)
        image.save(imgfile_name, "JPEG")

    # Delete originals
    print("Deleting original pdfs...")
    for f in imgfiles:
        os.remove(f)

if pdffiles is not None:
    # Do work on pdf files
    for pdf in pdffiles:
        # Do modifications for filename
        pdffile_rpl1 = os.path.splitext(pdf)[0] + ".jpg"
        pdffile_name = pdffile_rpl1.replace("full_", "")
        print("Converting ", pdffile_name)

        # Open pdf extract first page
        pdffile = pdfium.PdfDocument(pdf)
        # ---- Change the number below to get a different pdf page: .get_page(0) = first page, .get_page(1) = second page, etc.
        page = pdffile.get_page(1)
        pil_image = page.render_topil()
        pil_image.save(pdffile_name)
        page.close()
        pdffile.close()

        # Open image and create thumbnail
        image = Image.open(pdffile_name)
        image.thumbnail(MAX_SIZE)
        image.save(pdffile_name, "JPEG")

    # Delete originals
    print("Deleting original pdfs...")
    for pdf in pdffiles:
        os.remove(pdf)

