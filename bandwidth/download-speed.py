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
import statistics
import sys
import time

import downloadtester
import csv_parser

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
        "-s", "--silent", action="store_true", help="Don't print verbose output from the download process")
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
    if options.silent:
        tester.VERBOSE = False

    if not options.silent:
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
       filesize = round(tester.get_filesize()/1024/1024,2)
       results.append(result)
       print
       verboseprint("Downloaded file size: " + str(filesize) + " MB")
       verboseprint("\nAverage download speed: " + str(round(result*0.000001,2)) + " MB/s - " + str(round(result*0.000008,2)) + " Mbps\n")
       n += 1

    overall_speed = sum(results)/n
    median_speed = statistics.median(results)
    min_speed = min (results)
    max_speed = max (results)
    verboseprint("\nOverall Average download speed: " + str(round(overall_speed*0.000001,2)) + "MB/s - " + str(round(overall_speed*0.000008,2)) + "Mbps")
    verboseprint("Maximum download speed: " + str(round(max_speed*0.000001,2)) + "MB/s - " + str(round(max_speed*0.000008,2)) + "Mbps")
    verboseprint("Minimum download speed: " + str(round(min_speed*0.000001,2)) + "MB/s - " + str(round(min_speed*0.000008,2)) + "Mbps")
    verboseprint("Median download speed: " + str(round(median_speed*0.000001,2)) + "MB/s - " + str(round(median_speed*0.000008,2)) + "Mbps\n")

    #Create csv with test results
    if options.outfile:
        csv_file = os.path.join(scriptDir, options.outfile)
        date = time.strftime("%c")
        overall_headers = ["Date","URL","Size (MB)","Min (MB/s)","Min (Mbps)","Max (MB/s)","Max (Mbps)","Average (MB/s)", "Average (Mbps)", "Median (MB/sec)", "Median (Mbps)"]
        overall_values = [date,url,filesize, round(min_speed*0.000001,2), round(min_speed*0.000001,2), round(max_speed*0.000001,2), round(max_speed*0.000008,2),round(overall_speed*0.000001,2), round(overall_speed*0.000001,2), round(median_speed*0.000001,2), round(median_speed*0.000008,2)]
        overall = (overall_headers,overall_values)
        csv_parser.csv_parser(results,csv_file, overall, filesize)

if __name__ == "__main__":
    sys.exit(main())
