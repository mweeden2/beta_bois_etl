# Matt Weeden
# 9/27/2018

# This script collects and aggregates provider rosters recently uploaded to ShareFile
#   into a single csv file.

import argparse
import sys
import os
import pprint
import json
import requests
import csv


def main():

    # -----------------------------------------------------------------------------------------
    # argparser definition/setup
    # -----------------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="Present a directory of json identity files to the verato-proxy web "
                                                 "service")
    parser.add_argument("-v", "--verbose", help="be verbose about it", action="store_true")
    parser.add_argument("-i", "--input_dir", required=True, help="directory of json identity files")
    parser.add_argument("-o", "--output_file", required=True, help="filename (path) where resulting csv file will be "
                                                                   "created")
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)

    # Verato proxy web service endpoint
    url = "http://child.dev.myhealthaccess.net/verato-proxy/api/postIdentity"

    # Output dir (linkId results)
    linkIdsd = dict()

    # Open the input file directory
    for filename in os.listdir(args.input_dir):

        if (filename.endswith(".json")):
            with open(args.input_dir + "/" + filename, 'r') as f:
                data = json.loads(f.read())

                source = data['identity']['sources'][0]['name']
                nativeId = data['identity']['sources'][0]['id']

                r = requests.post(url, json=data)

                j = r.json()
                linkId = j['content']['linkId']
                if args.verbose:
                    print(source + ' ' + nativeId + ': ' + linkId)

                linkIdsd[linkId] = (source, nativeId)

    with open(args.output_file, 'w') as f:
        wtr = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        # write header row
        wtr.writerow(['source', 'nativeId', 'linkId'])
        # f.write('"source","nativeId","linkId"')

        for k, v in linkIdsd.items():
            wtr.writerow([v[0], v[1], k])


    return True


if __name__ == "__main__":
    main()
