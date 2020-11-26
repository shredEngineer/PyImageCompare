# PyImageCompare
# Copyright © 2020 by Paul Wilhelm <anfrage@paulwilhelm.de>
# https://github.com/shredEngineer/PyImageCompare

# Compares all JPEG images in a folder and renames (enumerates) duplicates. Differences in resolution and quality don't matter!

# This program loads all images in a folder, generates grayscale thumbnails and calculates the cross-image power.
# It then renames (enumerates) similar image pairs, such that you can examine and delete the duplicates afterwards.
# The "DUP_xxxx_A_…" files should always be the bigger ones, so you are probably safe to delete the "DUP_xxxx_B_…" files.

# Tested with Python 3.8 in Ubuntu 20.04

# Note: You should upgrade pillow if you get metadata errors:  python3 -m pip install pillow --upgrade

import os
import glob
from tqdm import tqdm
from si_prefix import si_format
from PIL import Image, ImageChops, ImageOps


# Set this to your image folder path
path = "/media/pw/EXTERN/FOTOS/2019 - Unsortiert"


# These settings worked very well for me
thumb_size = (128, 128)
power_threshold = 50


def main():

    # Scan the folder for JPG and JPEG images
    filenames = []
    for pattern in ["*.jpg", "*.jpeg"]:
        for filename in glob.glob(os.path.join(path, pattern)):
            filenames.append(filename)

    print()
    print(f"Loading images in path '{path}' …")
    print()
    thumbs = []
    for filename in tqdm(filenames, unit="images"):
        # Generating a grayscale thumbnail "normalizes" the image in terms of color, width and height
        thumb = ImageOps.exif_transpose(Image.open(filename))   # Load image, rotate according to EXIF orientation
        thumb.thumbnail(thumb_size, Image.ANTIALIAS)            # Generate thumbnail
        thumb = thumb.convert("L")                              # Convert to grayscale
        thumbs.append(thumb)

    print()
    print(f"Checking for similar image pairs, using thumbnail size = {thumb_size}, power threshold = {power_threshold} …")
    print()
    dup_count = 0
    for i in tqdm(range(0, len(filenames) - 1), unit="partition"):
        for j in tqdm(range(i + 1, len(filenames)), unit="images", leave=False):

            # Calculate the cross-image power
            image_diff = ImageChops.difference(thumbs[i], thumbs[j])
            power = image_power(image_diff)
            image_diff.close()

            if power < power_threshold:

                # Prioritize the larger image
                if os.path.getsize(filenames[i]) >= os.path.getsize(filenames[j]):
                    a, b = i, j
                else:
                    a, b = j, i

                dup_filename_a = os.path.join(os.path.dirname(filenames[a]), f"DUP_{dup_count:04d}_A_" + os.path.basename(filenames[a]))
                dup_filename_b = os.path.join(os.path.dirname(filenames[b]), f"DUP_{dup_count:04d}_B_" + os.path.basename(filenames[b]))

                message = \
                    f"#{dup_count:04d}:  " + \
                    "'" + os.path.basename(filenames[a]) + f"' ({si_format(os.path.getsize(filenames[a]))}B)" + \
                    "  is similar to  " + \
                    "'" + os.path.basename(filenames[b]) + f"' ({si_format(os.path.getsize(filenames[b]))}B)" + \
                    "  --  renaming to  " + \
                    "'" + os.path.basename(dup_filename_a) + f"'" + \
                    "  and  " + \
                    "'" + os.path.basename(dup_filename_b) + f"'"
                tqdm.write(message)

                dup_count += 1

                # Rename the files on disk and in our filename list
                os.rename(filenames[a], dup_filename_a)
                os.rename(filenames[b], dup_filename_b)
                filenames[a] = dup_filename_a
                filenames[b] = dup_filename_b

    print()
    print("Unloading images …")
    for i in tqdm(range(len(filenames)), unit=" images"):
        thumbs[i].close()

    print()
    print("DONE!")


def image_power(image_grayscale):
    # Calculate the normalized image power
    power = 0
    for x in range(image_grayscale.width):
        for y in range(image_grayscale.height):
            power += image_grayscale.getpixel((x, y)) ** 2
    image_grayscale.close()
    return power / image_grayscale.width / image_grayscale.height


if __name__ == "__main__":
    main()
