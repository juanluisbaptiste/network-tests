#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

#from __future__ import print_function

import argparse
import numpy
import os
import pkg_resources  # part of setuptools
import signal
import statistics
import sys
import time

import uploadtester
import csv_parser

tester = uploadtester.UploadTester()
version = pkg_resources.require("network-tests")[0].version

def parse_option():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--count", required=False, help="Number of uploads to do. Default: " + str(tester.DEFAULT_UPLOAD_COUNT))
    parser.add_argument(
        "-f", "--uploadfile", required=True, help="Test file to upload")
    parser.add_argument(
        "-o", "--outfile", required=False, help="Destination file for test results in CSV format")
    parser.add_argument(
        "-s", "--silent", action="store_true", help="Don't print verbose output from the upload process")
    parser.add_argument(
        "-l", "--host", required=True, help="FTP server for upload test")
    parser.add_argument(
        "-u", "--username", required=True, help="FTP user name for upload test")
    parser.add_argument(
        "-p", "--password", required=True, help="FTP password for upload test")
    parser.add_argument(
        "-P", "--passive", required=False, help="Sets FTP passive mode. Default: " + str(tester.passive))
    parser.add_argument(
        "-V", "--version", action="version", version="Program Version: " + version, help="Print program version")

    return parser.parse_args()

def signal_handler(signal, frame):
        print '\n\nTest cancelled!\n'
        tester.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    options = parse_option()
    tester.host = options.host
    tester.username = options.username
    tester.password = options.password
    filesize = float(os.path.getsize(options.uploadfile))
    scriptDir = sys.path[0]

    if options.passive == "yes":
        tester.passive = True
    if options.silent:
        tester.VERBOSE = False
    if tester.VERBOSE:
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
    verboseprint('File: ' + options.uploadfile)
    filesize = round(filesize/1024/1024,2) #size in MB
    verboseprint('Size: ' + str(filesize) + "MB")
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
       verboseprint("\nAverage upload speed: " + str(round(result*0.000001,2)) + "MB/s - " + str(round(result*0.000008,2)) + "Mbps\n")
       n += 1

    overall_speed = sum(results)/n
    median_speed = statistics.median(results)
    deviation = numpy.std(results)
    min_speed = min (results)
    max_speed = max (results)
    verboseprint("\nTest Results:")
    verboseprint("---- -------\n")
    verboseprint("Time Elapsed: " + str(tester.overall_time_elapsed) + " seconds\n")
    verboseprint("Overall Average download speed: " + str(round(overall_speed*0.000001,2)) + "MB/s - " + str(round(overall_speed*0.000008,2)) + "Mbps")
    verboseprint("Maximum download speed: " + str(round(max_speed*0.000001,2)) + "MB/s - " + str(round(max_speed*0.000008,2)) + "Mbps")
    verboseprint("Minimum download speed: " + str(round(min_speed*0.000001,2)) + "MB/s - " + str(round(min_speed*0.000008,2)) + "Mbps")
    verboseprint("Median download speed: " + str(round(median_speed*0.000001,2)) + "MB/s - " + str(round(median_speed*0.000008,2)) + "Mbps")
    verboseprint("Standard Deviation: " + str(round(deviation*0.000001,2)) + "MB/s - " + str(round(deviation*0.000008,2)) + "Mbps\n")

    #Create csv with test results
    if options.outfile:
        csv_file = os.path.join(scriptDir, options.outfile)
        date = time.strftime("%c")
        overall_headers = ["Date","Server","File","Size","Min (MB/s)","Min (Mbps)","Max (MB/s)","Max (Mbps)","Average (MB/s)", "Average (Mbps)", "Median (MB/sec)", "Median (Mbps)", "Deviation (MB/sec)", "Deviation (Mbps)"]
        overall_values = [date,options.host,options.uploadfile,filesize,round(min_speed*0.000001,2), round(min_speed*0.000001,2), round(max_speed*0.000001,2), round(max_speed*0.000008,2),round(overall_speed*0.000001,2), round(overall_speed*0.000008,2), round(median_speed*0.000001,2), round(median_speed*0.000008,2), round(deviation*0.000001,2), round(deviation*0.000008,2)]
        overall = (overall_headers,overall_values)
        csv_parser.csv_parser(results,csv_file, overall,filesize)
    #Cleanup everything
    tester.cleanup()

if __name__ == "__main__":
    sys.exit(main())
