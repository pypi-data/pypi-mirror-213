#!/usr/bin/bash

# Stop script on error
set -e

###################################################
#
# Set the splash of a Debian OS to the desired image
#
###################################################

# Define relevant variables
PLYMOUTH_APP="plymouth-themes"
PLYMOUTH_SCRIPT="/etc/alternatives/default.plymouth"
PLYMOUTH_THEME_DIR="/usr/share/plymouth/themes"
REPLACEMENT_IMAGE=$1

# Ensure the user has the proper permissions
if [ "$EUID" -ne 0 ]
then echo "Please run as root"
     exit
fi

# test print the user
# echo "User is: $USER"

# Ensure the user has provided an image
if [ -z "$REPLACEMENT_IMAGE" ]
then echo "Please provide an image"
     exit
fi

# Ensure the image exists
if [ ! -f "$REPLACEMENT_IMAGE" ]
then echo "Image does not exist"
     exit
fi

# Ensure the image is a png
if [ ${REPLACEMENT_IMAGE: -4} != ".png" ]
then echo "Image must be a png"
     exit
fi

# Install the plymouth themes if not already installed
if ! dpkg -s $PLYMOUTH_APP > /dev/null 2>&1; then
    apt install $PLYMOUTH_APP
fi

# Read the contents of the script and capture the ImageDir path
IMAGE_DIR=$(grep "ImageDir" $PLYMOUTH_SCRIPT | cut -d "/" -f6)

# Insert the image in the plymouth IMAGE_DIR with th name "watermark.png"
cp $REPLACEMENT_IMAGE $PLYMOUTH_THEME_DIR/$IMAGE_DIR/watermark.png


