import argparse
from imutils import paths
import requests
import cv2
import os
import pathlib as pl

# initialize the directory
data_folder = pl.Path(pl.PureWindowsPath('f:\\Work\\Pycharm_Projects\\'
                                   'Recycling_Paper\\images\\MC-1A'))

# initialize the index of the latest 'image_save'
total_number = []
for current_file in data_folder.iterdir():
    total_number.append(current_file.stem)
total = int(max(total_number)) + 1

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--urls', required=True)
parser.add_argument('-o', '--output', required=True)
args = vars(parser.parse_args())

# grab the list of URLs from the input file, then initialize the
# total number of images downloaded thus far
rows = open(args["urls"]).read().strip().split("\n")

# loop the URLs
for url in rows:
    try:
        # try to download the image
        image_download = requests.get(url, timeout=60)

        # save the image to disk
        image_save = os.path.sep.join([args['output'], '{0}.jpg'.format(
            str(total).zfill(8))])
        image_open = open(image_save, 'wb')
        image_open.write(image_download.content)
        image_open.close()

        # update the counter
        print("[INFO] downloaded: {}".format(image_save))
        total += 1

    # handle if any exceptions are thrown during the downloaded process
    except:
        print("[INFO] error downloading {0}...skipping".format(image_save))

# loop over the image paths we just downloaded
for imagePath in paths.list_images(args["output"]):
    # initialize if the image should be deleted or not
    delete = False

    # try to load the image
    try:
        image = cv2.imread(imagePath)

        # if the image is `None` then we could not properly load it
        # from disk, so delete it
        if image is None:
            delete = True

    # if OpenCV cannot load the image then the image is likely
    # corrupt so we should delete it
    except:
        print("Except")
        delete = True

    # check to see if the image should be deleted
    if delete:
        print("[INFO] deleting {}".format(imagePath))
        os.remove(imagePath)