#!/bin/bash

# Show internal hyperlinks

if [ "$#" -ne 1 ] ; then
  echo "Usage: showinternallinks.sh rootDirectory" >&2
  exit 1
fi

rootDir=$1
postsDir=$rootDir"/_posts"

while IFS= read -d $'\0' file ; do
    echo "*****"$file"*****"
    echo
    # Extract all image links and split into array
    #links=$(grep -Po '(\[(.*?)\]\((.*?)\))' $file)
    links=$(grep -Po '(\[(.*?)\]\((.*?BASE_PATH.*?)\))' $file)
    echo $links
    echo

done < <(find $postsDir -type f -print0)
