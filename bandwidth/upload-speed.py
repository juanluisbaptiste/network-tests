#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

#from __future__ import print_function

import argparse
import os
import signal
import sys

import uploadtester

tester = uploadtester.UploadTester()

def parse_option():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--count", required=False, help="Number of uploads to do. Default: " + str(tester.DEFAULT_UPLOAD_COUNT))
    parser.add_argument(
        "-f", "--uploadfile", required=True, help="Test file to upload")
    parser.add_argument(
        "-o", "--outfile", required=False, help="Destination file for test results in CSV format")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print verbose output from the download process")
    parser.add_argument(
        "-l", "--host", required=True, help="FTP server for upload test")
    parser.add_argument(
        "-u", "--username", required=True, help="FTP user name for upload test")
    parser.add_argument(
        "-p", "--password", required=True, help="FTP password for upload test")
    parser.add_argument(
        "-P", "--passive", required=False, help="Sets FTP passive mode. Default: " + str(tester.passive))

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
    tester.host = options.host
    tester.username = options.username
    tester.password = options.password
    filesize = float(os.path.getsize(options.uploadfile))

    if options.passive == "yes":
        tester.passive = True

    scriptDir = sys.path[0]

    if options.verbose:
        def verboseprint(*args):
            # Print each argument separately so caller doesn't need to
            # stuff everything to be printed into a single string
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None      # do-nothing function

    verboseprint('FTP Host: ' + options.host)
    verboseprint('Username: ' + tester.username)
    verboseprint('Password: ' + tester.password)
    verboseprint('\nFile: ' + options.uploadfile)
    verboseprint('File Size: ' + str(round(filesize/1024/1024,2)) + "MB")
    num_tests = int(options.count or tester.DEFAULT_UPLOAD_COUNT)
    verboseprint('\nTotal Tests: ' + str(num_tests))
    print

    results = []
    n = 0
    #Do tests
    while (n < num_tests):
       verboseprint ('Test #' + str(n + 1) + ': ')
       result = tester.upload_file(options.uploadfile)
       results.append(result)
       print
       verboseprint("\nAverage upload speed: " + str(round(result[0],2)) + "MB/s\n")
       n += 1

    print
    #Create csv with test results
    if options.outfile:
        csv_file = os.path.join(scriptDir, options.outfile)
        tester.csv_parser(results,csv_file)

if __name__ == "__main__":
    sys.exit(main())
