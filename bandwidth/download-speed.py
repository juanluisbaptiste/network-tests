#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

# Inspired on netspeed.sh script from https://bitbucket.org/rsvp/gists/src

#from __future__ import print_function

import argparse
import os
import signal
import sys

import downloadtester

tester = downloadtester.DownloadTester()

def parse_option():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--count", required=False, help="Number of downloads to do. Default: " + str(tester.DEFAULT_DOWNLOAD_COUNT))
    parser.add_argument(
        "-l", "--location", required=False, help="Server location for the test. Default: " + str(tester.DEFAULT_LOCATION), choices=tester.locations)
    parser.add_argument(
        "-o", "--outfile", required=False, help="Destination file for test results in CSV format")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print verbose output from the download process")
    parser.add_argument(
        "-u", "--url", required=False, help="Alternate download URL (it must include path and filename)")

    return parser.parse_args()

def signal_handler(signal, frame):
        print '\n\nTest cancelled!\n'
        tester.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    options = parse_option()
    #global functions.VERBOSE
    tester.VERBOSE = options.verbose

    if options.verbose:
        def verboseprint(*args):
            # Print each argument separately so caller doesn't need to
            # stuff everything to be printed into a single string
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None      # do-nothing function

    #Set download location
    location = options.location or tester.DEFAULT_LOCATION
    scriptDir = sys.path[0]

    #Overwrite with custom URL
    if not options.url:
        verboseprint('Location: ' + location)
        url = tester.get_location(location)
    else:
        url = options.url
    verboseprint('URL: ' + url)
    num_tests = int(options.count or tester.DEFAULT_DOWNLOAD_COUNT)
    verboseprint('Total Tests: ' + str(num_tests))
    print

    results = []
    n = 0
    #Do tests
    while (n < num_tests):
       verboseprint ('Test #' + str(n + 1) + ': ')
       result = tester.download_file(url)
       results.append(result)
       print
       verboseprint("\nAverage download speed: " + str(round(result[0],2)) + "MB/s\n")
       n += 1

    print
    #Create csv with test results
    if options.outfile:
        csv_file = os.path.join(scriptDir, options.outfile)
        tester.csv_parser(results,csv_file)

if __name__ == "__main__":
    sys.exit(main())
