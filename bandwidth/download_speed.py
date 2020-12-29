#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

# Inspired on netspeed.sh script from https://bitbucket.org/rsvp/gists/src

# from __future__ import print_function

import argparse
import numpy
import os
import pkg_resources
import signal
import statistics
import sys
import time
from urllib.request import urlopen

import common
from . import downloadtester
from . import csv_parser

tester = downloadtester.DownloadTester()
try:
    version = pkg_resources.require("network-tests")[0].version
except pkg_resources.DistributionNotFound:
    version = "dev"


def parse_option():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--count", required=False, help="Number of downloads to do. \
        Default: " + str(tester.DEFAULT_DOWNLOAD_COUNT))
    parser.add_argument(
        "-l", "--location", required=False, help="Server location for the \
        test. Default: " + str(tester.DEFAULT_LOCATION),
        choices=tester.locations)
    parser.add_argument(
        "-o", "--outfile", required=False, help="Destination file for test \
        results in CSV format")
    parser.add_argument(
        "-s", "--silent", action="store_true", help="Don't print verbose \
        output from the download process")
    parser.add_argument(
        "-u", "--url", required=False, help="Alternate download URL (it must \
        include path and filename)")
    parser.add_argument(
        "-V", "--version", action="version", version="Program \
        Version: " + version, help="Print program version")

    return parser.parse_args()


def signal_handler(signal, frame):
        """Signal handler."""
        print ('\n\nTest cancelled!\n')
        tester.cleanup()
        sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    """Run main program."""
    # global functions.VERBOSE
    options = parse_option()
    if options.silent:
        tester.VERBOSE = False

    if not options.silent:
        def verboseprint(*args):
            # Print each argument separately so caller doesn't need to
            # stuff everything to be printed into a single string
            for arg in args:
                print (arg),
            print
    else:
        verboseprint = lambda *a: None      # do-nothing function

    # Set download location
    location = options.location or tester.DEFAULT_LOCATION
    # Print the program version
    verboseprint(os.path.basename(__file__) + ' ' + version + '\n')

    # Overwrite with custom URL
    if not options.url:
        verboseprint('Location: ' + location)
        url = tester.get_location(location)
    else:
        try:
            urllib2.urlopen(options.url)
        except Exception:
            print ("ERROR: Download URL does not exist.")
            sys.exit(1)
        url = options.url
    verboseprint('URL: ' + url)

    # Check that output dir exists
    if (
        options.outfile and not
        os.path.exists(os.path.dirname(options.outfile))
       ):
        print ("\nERROR: Output file destination directory does not \
        exist: " + os.path.dirname(options.outfile) + " \n")
        sys.exit(1)

    num_tests = int(options.count or tester.DEFAULT_DOWNLOAD_COUNT)
    verboseprint('Total Tests: ' + str(num_tests))
    print

    results = []
    n = 0
    # Do tests
    while (n < num_tests):
        verboseprint('Test #' + str(n + 1) + ': ')
        result = tester.download_file(url)
        filesize = round(tester.get_filesize()/1024/1024, 2)
        results.append(result)
        verboseprint("\nDownloaded file size: " + str(filesize) + " MB")
        verboseprint("\nAverage download speed: " +
                     str(round(result*common.SPEED_MB_SEC, 2)) + " MB/s - " +
                     str(round(result*common.SPEED_MBIT_SEC, 2)) + " Mbps\n")
        n += 1

    overall_speed = sum(results)/n
    median_speed = statistics.median(results)
    deviation = numpy.std(results)
    min_speed = min(results)
    max_speed = max(results)
    verboseprint("\nTest Results:")
    verboseprint("---- -------\n")
    verboseprint("Time Elapsed: " + str(tester.overall_time_elapsed) +
                 " seconds\n")
    verboseprint("Overall Average Download Speed: " +
                 str(round(overall_speed*common.SPEED_MB_SEC, 2)) +
                 "MB/s - " +
                 str(round(overall_speed*common.SPEED_MBIT_SEC, 2)) + "Mbps")
    verboseprint("Maximum download speed: " +
                 str(round(max_speed*common.SPEED_MB_SEC, 2)) + "MB/s - " +
                 str(round(max_speed*common.SPEED_MBIT_SEC, 2)) + "Mbps")
    verboseprint("Minimum download speed: " +
                 str(round(min_speed*common.SPEED_MB_SEC, 2)) + "MB/s - " +
                 str(round(min_speed*common.SPEED_MBIT_SEC, 2)) + "Mbps")
    verboseprint("Median download speed: " +
                 str(round(median_speed*common.SPEED_MB_SEC, 2)) + "MB/s - " +
                 str(round(median_speed*common.SPEED_MBIT_SEC, 2)) + "Mbps")
    verboseprint("Standard Deviation: " +
                 str(round(deviation*common.SPEED_MB_SEC, 2)) + "MB/s - " +
                 str(round(deviation*common.SPEED_MBIT_SEC, 2)) + "Mbps\n")

    # Create csv with test results
    if options.outfile:
        scriptDir = os.getcwd()
        csv_file = os.path.join(scriptDir, options.outfile)
        date = time.strftime("%c")
        overall_headers = ["Date",
                           "URL",
                           "Size (MB)",
                           "Min (MB/s)",
                           "Min (Mbps)",
                           "Max (MB/s)",
                           "Max (Mbps)",
                           "Average (MB/s)",
                           "Average (Mbps)",
                           "Median (MB/s)",
                           "Median (Mbps)",
                           "Deviation (MB/s)",
                           "Deviation (Mbps)",
                           "Program Version"]
        overall_values = [date,
                          url,
                          filesize,
                          round(min_speed*common.SPEED_MB_SEC, 2),
                          round(min_speed*common.SPEED_MBIT_SEC, 2),
                          round(max_speed*common.SPEED_MB_SEC, 2),
                          round(max_speed*common.SPEED_MBIT_SEC, 2),
                          round(overall_speed*common.SPEED_MB_SEC, 2),
                          round(overall_speed*common.SPEED_MBIT_SEC, 2),
                          round(median_speed*common.SPEED_MB_SEC, 2),
                          round(median_speed*common.SPEED_MBIT_SEC, 2),
                          round(deviation*common.SPEED_MB_SEC, 2),
                          round(deviation*common.SPEED_MBIT_SEC, 2),
                          "v" + version]
        overall = (overall_headers, overall_values)
        csv_parser.csv_parser(results, csv_file, overall, filesize)


if __name__ == "__main__":
    sys.exit(main())
