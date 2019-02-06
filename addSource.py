#! /usr/bin/env python3

import os
import sys
import glob
import csv
import urllib.request


def processBlog(urlDidl, csvOut):
    """Process one DIDL and write results to csvOut"""

    # Parse DIDL
    urls = parseDidl(urlDidl)
    
    # Iterate over urls
    for inURL in urls:
        try:
            # Open URL location, response to file-like object 'response'                         
            response = urllib.request.urlopen(inURL)
            
            # Status code
            httpStatus = str(response.getcode())

            # Output URL (can be different from inURL in case of redirection)
            outURL=response.geturl()

            # HTTP headers
            headers = response.info()

            # Data (i.e. the actual object that is retrieved)
            data = response.read()

            # Content-Disposition header
            contentDisposition = headers['Content-Disposition']
            if not contentDisposition: 
                contentDisposition = "n/a"
                
            # Content-Type header
            contentType = headers['Content-Type']
            if not contentType:
                contentType = "n/a"

        except urllib.error.HTTPError as e:
            httpStatus = str(e)
            outURL = "n/a"
            contentDisposition = "n/a"
            contentType = "n/a"

        except urllib.error.URLError as e:
            httpStatus = str(e)
            outURL = "n/a"
            contentDisposition = "n/a"
            contentType = "n/a"

        # Write record to output file
        csvOut.writerow([inURL,httpStatus, outURL,contentDisposition, contentType])

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
            print(postName, originStr)

    """

    # Open input file (one DIDL link per line)
    dirPosts = sys.argv[1]
    fIn = open(fileIn, "r", encoding="utf-8")
    # Content to list (each item represents 1 DIDL URL)
    didls = fIn.read().splitlines()
    fIn.close()

     # Open output file and create CSV writer object
    fileOut = sys.argv[2]
    fOut = open(fileOut, "w", encoding="utf-8")
    csvOut = csv.writer(fOut, lineterminator='\n')
    
    # Write header line to output file
    csvOut.writerow(["URLIn", "httpStatus", "URLOut", "Content-Disposition", "Content-Type"])

    # Iterate over didl files
    for didl in didls:
        if didl != "":
            processDIDL(didl,csvOut)

    # Close output file
    fOut.close()
    """

if __name__ == "__main__":
    main()
