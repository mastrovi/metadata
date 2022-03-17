import os, requests, csv, shutil, time, mimetypes
from lxml import html
import urllib.request


def image_downloader(file: object):
    """
    This Function Downloads images from a csv structured:
        record_id,url
    Args:
        file: the path of the text file.
    On Execution:
        Downloads the images from URLs provided on the text file
        and saves them in a directory with the same filename as the csv.
    Raises:
        ValueError or URLError if url is incorrect or unknown url type.
    """
    # Strip quotes if they exist

    # Gets directory of input csv
    work_dir = os.path.dirname(file)
    # Gets filename without extension
    base = os.path.basename(file)
    # Appends filename to directory path
    thumb_dir = work_dir + '/' + os.path.splitext(base)[0]

    # Creates thumbnail directory
    if not os.path.exists(thumb_dir):
        # if directory Doesnt Exist Create it.
        os.makedirs(thumb_dir)

    # Change to thumbnail directory to do the work
    os.chdir(thumb_dir)

    # Do work
    with open(file, "r") as read_obj:
        csv_dict_reader = csv.DictReader(read_obj)

        # Start counters for downloads
        success_counter = 0
        fail_counter = 0

        for row in csv_dict_reader:
            file_name = row["record_id"]
            url1 = row["url"]
            url2 = row["url2"]

            r = requests.get(url1, stream=True)
            manifest = r.json()
            try:
                page1 = manifest['sequences'][0]['canvases'][1]['images'][0]['resource']['@id']

                # Check if the first page url responds and if so, do work
                firstImage = requests.get(page1, headers={'Referer': page1}, stream=True)
                if firstImage.status_code == 200:
                    extension = mimetypes.guess_extension(firstImage.headers.get('content-type', '').split(';')[0])
                    # print(extension)
                    full_name = "full_" + file_name + extension

                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    firstImage.raw.decode_content = True

                    # Open a local file with wb ( write binary ) permission.
                    with open(full_name, 'wb') as f:
                        shutil.copyfileobj(firstImage.raw, f)

                    # Add to counter
                    success_counter += 1
                    print(file_name, ' successfully downloaded')

                    # Pause for a half second to be kinder to the server
                    time.sleep(.5)

                else:
                    print('Image Couldn\'t be retreived ', file_name)
                    # Add to counter
                    fail_counter += 1

                    # Open text file and append filename and url
                    fail_text = open("failed.txt", "a")
                    fail_text.writelines(file_name + "," + page1 + "\n")
                    fail_text.close()

                    # Pause for a half second to be kinder to the server
                    time.sleep(.5)
            except:
                print('Image Couldn\'t be retreived ', file_name)
                # Add to counter
                fail_counter += 1

                # Open text file and append filename and url
                fail_text = open("failed.txt", "a")
                fail_text.writelines(file_name + "," + url1 + "\n")
                fail_text.close()

                # Pause for a half second to be kinder to the server
                time.sleep(.5)
                continue


        # Print statement to confirm quantity of successful downloads
        if (fail_counter == 0):
            print("All ", success_counter, " items successfully downloaded")
        elif (fail_counter > 0) and (success_counter > 0):
            print(success_counter, ' images successfully downloaded')
            print(fail_counter, ' downloads failed. Please see failed.txt')
        else:
            print(fail_counter, ' downloads failed. Please see failed.txt')


if __name__ == '__main__':
    input_file = input("Input the collectionSlug.csv with two values: record_id,url: ")
    input_file = input_file.strip('\"')
    image_downloader(input_file)