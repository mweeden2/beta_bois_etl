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

    # Output dict (results)
    messagesD = dict()

    # Call for all the messages
    done = False
    while not done:

        r = requests.get(url)

        j = r.json()
        if args.verbose:
            # pp.pprint([x for x in j['response']['messages']][0])
            pass
        count = 0
        for m in j['response']['messages']:
            count += 1
            if args.verbose:
                print(f"capturing message {count} of {len(j['response']['messages'])}")
            messagesD[m['id']] = m
        done = True


    with open(args.output_file, 'w') as f:

        fieldnames = messagesD.values[0].keys()

        pp.pprint(fieldnames)
        return

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()

        for k, v in messagesD.items():
            #wtr.writerow([v[0], v[1], k])
            writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})



    return True


if __name__ == "__main__":
    main()
