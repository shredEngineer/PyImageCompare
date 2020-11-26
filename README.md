# PyImageCompare

Copyright (C) 2020 by Paul Wilhelm <<anfrage@paulwilhelm.de>>

Compares all JPEG images in a folder and renames (enumerates) duplicates. Differences in resolution and quality don't matter!

This program loads all images in a folder, generates grayscale thumbnails and calculates the cross-image power.

It then renames (enumerates) similar image pairs such that you can examine and delete the duplicates afterwards.

The "DUP_xxxx_A" file should always be the bigger one, so you are probably safe to delete the "DUP_xxxx_B" files.

*Tested with Python 3.8 in Ubuntu 20.04*

*Note:* You should upgrade pillow if you get metadata errors:  python3 -m pip install pillow --upgrade
