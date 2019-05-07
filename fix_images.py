import cv2
import numpy as np
import undistort
import glob
import os


def fixAndMerge(*images):
    """
    Applies fish-eye un-distortions to given images, cut properly and combines them vertically.
    :param images: is the images to be fixed and merged.
    :return: fixed and combined image.
    """
    assert len(images) == 3, "Number of images exceeded!"

    fixed = [undistort.undistort(img) for img in images]

    # Cut images appropriately.
    fixed[0] = cutImage(fixed[0], y2=360)
    fixed[1] = cutImage(fixed[1], y1=120)
    fixed[2] = cutImage(fixed[2], y2=360)

    # Stack vertically.
    return np.concatenate(fixed, axis=0)


def fileGroup(filename):
    """ Cuts 'filename_1.png' to the string 'filename'. """
    return filename[:-6]


def cutImage(img, y1=0, y2=480):
    return img[0:640][y1:y2]


def getImageDict(path_pattern):
    """ Gets the dict of images having path_pattern = '*_1.png' or '*_2.png' etc. """
    files = glob.glob(path_pattern)

    return {fileGroup(file): cv2.imread(file) for file in files}


data_folder = "dataset"
images_part1 = getImageDict(data_folder + "/*_0.png")
images_part2 = getImageDict(data_folder + "/*_1.png")
images_part3 = getImageDict(data_folder + "/*_2.png")

# Create output directory.
output_folder = os.path.join(os.getcwd(), "output")
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

print("Processing...")
total = 0
for file_name in images_part1:
    # Fix and combine the image parts.
    img1 = images_part1.get(file_name)
    img2 = images_part2.get(file_name)
    img3 = images_part3.get(file_name)

    if img3 is None or img2 is None:
        print("Some part of images were missing...")
        print("Skipping...")
        continue

    final_img = fixAndMerge(img1, img2, img3)

    # Finalize the output path.
    final_name = file_name[8:] + ".png"
    final_name = os.path.join(output_folder, final_name)

    # Write to output.
    cv2.imwrite(final_name, final_img)
    total += 1
    print("%{0} processed...".format(total * 100 / len(images_part1)))

print("Done... \nCheck the file for output:{0}".format(output_folder))