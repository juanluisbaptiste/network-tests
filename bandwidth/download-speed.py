#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

# Inspired on netspeed.sh script from https://bitbucket.org/rsvp/gists/src

#from __future__ import print_function

import argparse
import os
import requests
import sys
import time

DEFAULT_LOCATION = "use"
DEFAULT_DOWNLOAD_COUNT = 1
VERBOSE = False

locations = {
             'london': 'http://speedtest.london.linode.com/100MB-london.bin',
             'sanjose': 'http://speedtest.sjc01.softlayer.com/speedtest/speedtest/random500x500.jpg' ,
             'tokyo': 'http://speedtest.tokyo.linode.com/100MB-tokyo.bin',
             'use': 'http://speedtest.newark.linode.com/100MB-newark.bin',
             'usw': 'http://speedtest.fremont.linode.com/100MB-fremont.bin',
             'washington': 'http://speedtest.wdc01.softlayer.com/downloads/test500.zip'
             }

def parse_option():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--count", required=False, help="Number of downloads to do. Default: " + str(DEFAULT_DOWNLOAD_COUNT))
    parser.add_argument(
        "-l", "--location", required=False, help="Server location for the test. Default: " + str(DEFAULT_LOCATION), choices=locations)
    parser.add_argument(
        "-o", "--outfile", required=False, help="Destination file for test results in CSV format")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print verbose output from the download process")
    parser.add_argument(
        "-u", "--url", required=False, help="Alternate download URL (it must include path and filename)")

    return parser.parse_args()

def get_download_url(location=DEFAULT_LOCATION):
    return locations.get(location)

def download_file(url, directory) :
  localFilename = url.split('/')[-1]
  global VERBOSE
  with open(directory + '/' + localFilename, 'wb') as f:
    dl = 0
    dl_speed = 0
    start = time.clock()
    r = requests.get(url, stream=True)
    total_length = r.headers.get('content-length')

    if total_length is None: # no content length header
      f.write(r.content)
    else:
      for chunk in r.iter_content(1024):
        dl += len(chunk)
        f.write(chunk)
        done = int(50 * dl / int(total_length))
        dl_speed = dl/(time.clock() - start)
        #Convert to MB/s when printing
        if VERBOSE:
          sys.stdout.write("\r[%s%s] %s MB/s" % ('=' * done, ' ' * (50-done), round(dl_speed/8000000,2)))
          sys.stdout.flush()
      time_elapsed = (time.clock() - start)
      avr_speed = (dl/time_elapsed)/8000000
      cleanup()
  return avr_speed

def cleanup():
  #Cleanup
  os.remove("/tmp/" + localFilename)


def csv_parser(results, csv_file):
    with open(csv_file, 'wb') as myfile:
        wr = csv.writer(myfile)
        header = ["Muestra", "Tamaño", "Velocidad Promedio (MB/sec)"]
        wr.writerow(header)
        for result in results:
            row = [result[1].packet_loss_count,result[1].packet_loss_rate,result[1].rtt_min,result[1].rtt_max,result[1].rtt_avg,result[0]]
            wr.writerow(row)
            print (result[0])
            print_ping_parser(result[1])

# def verboseprint(*args):
#     # Print each argument separately so caller doesn't need to
#     # stuff everything to be printed into a single string
#     for arg in args:
#        print arg,
#     print

def main():
    options = parse_option()
    global VERBOSE
    VERBOSE = options.verbose
    if VERBOSE:
        def verboseprint(*args):
            # Print each argument separately so caller doesn't need to
            # stuff everything to be printed into a single string
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None      # do-nothing function

    location = options.location or DEFAULT_LOCATION
    scriptDir = sys.path[0]

    if not options.url:
        verboseprint('Location: ' + location)
        url = get_download_url(location)
    else:
        url = options.url
    verboseprint('URL: ' + url)
    num_tests = int(options.count or DEFAULT_DOWNLOAD_COUNT)
    verboseprint('Total Tests: ' + str(num_tests))
    print
    n = 0
    while (n < num_tests):
       verboseprint ('Test #' + str(n + 1) + ': ')
       avr_speed = download_file(url, "/tmp")
       print
       verboseprint("\nAverage download speed: " + str(round(avr_speed,2)) + "MB/s\n")
       n += 1

    print
    print options.outfile
    #csv_file = os.path.join(scriptDir, options.outfile)
if __name__ == "__main__":
    sys.exit(main())
