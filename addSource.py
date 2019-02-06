#! /usr/bin/env python3

import os
import sys
import glob
import urllib.request

def main():

    # CLI I/O
    if len(sys.argv) != 2:
        print("USAGE: addSource.py diPosts")
        sys.exit()
  
    opfBaseURL = 'https://openpreservation.org/blog/'
    kbBaseURL = 'http://blog.kbresearch.nl/'

    postsDir = os.path.normpath(sys.argv[1])
    posts = glob.glob(postsDir + "/*")

    for post in posts:
        postName = os.path.basename(post).split('.')[0]
        urlPattern = postName.replace('-', '/', 3) + '/'
        urlOPF = opfBaseURL + urlPattern
        urlKB = kbBaseURL + urlPattern

        try:
            # Open URL location, response to file-like object 'response'                         
            responseOPF = urllib.request.urlopen(urlOPF)
            # Status code
            statusOPF = str(responseOPF.getcode())
        
        except:
            statusOPF = 'n/a'

        try:
            # Open URL location, response to file-like object 'response'                         
            responseKB = urllib.request.urlopen(urlKB)
            # Status code
            statusKB = str(responseKB.getcode())
        
        except:
            statusKB = 'n/a'

        originStr = ''

        if statusOPF == "200":
            originStr = '\n<hr>\nOriginally published at the [Open Preservation Foundation blog](' + urlOPF + ')\n'
        elif statusKB == "200":
            originStr = '\n<hr>\nOriginally published at the [KB Research blog](' + urlKB + ')\n'
        
        if originStr != '':
            # Append string to blog
            with open(post, "a") as fPost:
                fPost.write(originStr)

if __name__ == "__main__":
    main()
