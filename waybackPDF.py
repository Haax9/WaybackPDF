#!/usr/bin/env python3
# coding: utf-8

import json
import os
import re
import requests
import argparse

class PC:
    """PC (Print Color)
    Used to generate some colorful, relevant, nicely formatted status messages.
    """
    green = '\033[92m'
    blue = '\033[94m'
    orange = '\033[93m'
    endc = '\033[0m'
    ok_box = blue + '[*] ' + endc
    note_box = green + '[+] ' + endc
    warn_box = orange + '[!] ' + endc


def parse_arguments():
    desc = ('OSINT tool to download archived PDF files from archive.org for'
            ' a given website.')
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-d', '--domain', type=str, action='store',
                        required=True,
                        help='The target domain you are looking for files')
    parser.add_argument('-o', '--output', type=str, action='store',
                        required=False,
                        help='Optional output directory (Default is the domain name)')
    parser.add_argument('--http', type=str, action='store',
                        required=False,
                        help='Use HTTP instead of HTTPS for the target domain.'
                        ' The default behavior uses HTTPS')
    parser.add_argument('-r', '--resume', type=int, action='store', required=False,
                        help='Start downloading at a given index and skip X previous'
                        ' files')

    args = parser.parse_args()
    return args


def getPDFlist(domain, protocol):
    print("\n" + PC.ok_box + "Requesting PDF list...")

    # Default target is HTTPS
    targetDomain = "https://{}".format(domain)

    # Building URL
    if protocol:
        targetDomain = "http://{}".format(domain)

    baseURL = "https://web.archive.org/web/timemap/"
    payload = {'url':targetDomain, 'matchType':'prefix','collapse':'urlkey',
               'output':'json', 'fl':'original,mimetype,timestamp,endtimestamp'
               ',groupcount,uniqcount', 'filter':'!statuscode:[45]..'
               ,'limit':'100000', '_':'1587473968806'}

    # HTTP request to get PDF list
    raw = requests.get(baseURL, params=payload).json()
    
    # Building the PDF list
    files = []
    headers = raw[0]
    
    for item in raw[1:]:
        file = {}
        for i, header in enumerate(headers):
            file[headers[i]] = item[i]
        files.append(file)
    pdfs = []
    
    for file in files:
        if file['mimetype'] == 'application/pdf':
            pdfs.append(file)
    
    for pdf in pdfs:
        # Create direct URL for each PDF
        pdf['wayback'] = 'https://web.archive.org/web/' + pdf['timestamp'] + 'if_/' + pdf['original']    
        name = pdf['original'].rsplit('/',1)[1]    

        if ".pdf" in name:
            name = name.rsplit(".", 1)    

        pdf['name'] = name[0] + '-' + pdf['timestamp']

    print(PC.note_box + "{} PDFs found".format(len(pdfs)))
    return pdfs


def downloadFiles(domain, pdfs, output, resume):
    # If needed, create directory
    if not os.path.exists(output):
        os.makedirs(output)

    print("\n" + PC.ok_box + "Downloading Files...")

    # Checking if resume switch is on
    if resume:
        print("\n" + PC.ok_box + "Resume switch on, skipping the first {} file(s)".format(resume))
        pdfs = pdfs[resume:]

    # Downloading and saving files
    for p,pdf in enumerate(pdfs): 
        outputDir = output + '/'
        fileName = pdf['name'][:250] + '.pdf'
        filePath = os.path.join(outputDir, fileName)
        with open(filePath,'wb') as file:
            data = requests.get(pdf['wayback'])
            file.write(data.content)
        print(PC.note_box + "({}/{}) Saved {}.pdf".format(p+1, len(pdfs),pdf['name']))


def main():
    """Main Function"""
    args = parse_arguments()

    if args.output:
        outputDir = args.output
    else:
        outputDir = args.domain

    print("\n" + PC.note_box + "Web Archive PDF Downloader ")
    print(PC.note_box + "Target domain : " + args.domain)
    print(PC.note_box + "Output directory : {}/".format(outputDir))

    # Getting the PDF list
    pdfList = getPDFlist(args.domain, args.http)

    # Downloading PDF
    downloadFiles(args.domain, pdfList, outputDir, args.resume)

    print("\n" + PC.ok_box + "Everything's done !")
    print(PC.ok_box + "Happy analysis !\n")


if __name__ == "__main__":
    main()