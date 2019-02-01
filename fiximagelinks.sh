#!/bin/bash

# Locate image links to all locally stored images in
# "images" folder, move these files to YYYY/MM subfolder
# and then update links in blog accordingly.

if [ "$#" -ne 1 ] ; then
  echo "Usage: fiximagelinks.sh rootDirectory" >&2
  exit 1
fi

rootDir=$1
postsDir=$rootDir"/_posts"
imageDirIn=$rootDir"/images"
imagePathStringIn="{{ BASE_PATH }}/images"

while IFS= read -d $'\0' file ; do
    bName=$(basename "$file")
    year="$(cut -d'-' -f1 <<<$bName)"
    month="$(cut -d'-' -f2 <<<$bName)"
    day="$(cut -d'-' -f3 <<<$bName)"

    # Sub-folder for each month
    imageDirOut=$imageDirIn"/"$year"/"$month
    imagePathStringOut=$imagePathStringIn"/"$year"/"$month
    
    # Create subfolder if it doesn't exist already
    if ! [ -d "$imageDirOut" ] ; then
        mkdir -p $imageDirOut
    fi

    # Extract all image links and split into array
    IFS='!'
    images=($(grep -Po '(?:!\[(.*?)\]\((.*?)\))' $file))
    unset IFS

    for image in "${images[@]}" ; do
        if [[ $image == *"BASE_PATH"* ]]; then
            imageName="$(cut -d')' -f1 <<<$image)"
            imageName="$(cut -d'/' -f3 <<<$imageName)"
            imageIn=$imageDirIn"/"$imageName
            imageOut=$imageDirOut"/"$imageName
            # Move image to output directory
            mv $imageIn $imageOut
        fi
    done

    # Update image links
    sed -i "s|$imagePathStringIn|$imagePathStringOut|g" $file

done < <(find $postsDir -type f -print0)
