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
    parser.add_argument("-o", "--output_file", required=True, help="filename (path) where resulting csv file will be "
                                                                   "created")
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)

    # Verato proxy web service endpoint
    base_url = "https://api.groupme.com/v3/groups/32181249/messages"

    # Get the GroupMe token
    token = os.environ["GROUPME_TOKEN"]

    # Construct the full url
    url = base_url + "?token=" + token

    # Output dir (linkId results)
    linkIdsd = dict()

    # Call for all the messages
    done = False
    while not done:

        r = requests.get(url)

        j = r.json()
        if args.verbose:
            pp.pprint(j)
        return


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
