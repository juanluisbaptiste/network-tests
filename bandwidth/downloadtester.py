#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

import csv
import os
import requests
import sys
import time

class DownloadTester():
    DEFAULT_LOCATION = "use"
    DEFAULT_DOWNLOAD_COUNT = 1
    VERBOSE = True
    localFilename = "100MB-newark.bin"
    locations = {
                 'london': 'http://speedtest.london.linode.com/100MB-london.bin',
                 'sanjose': 'http://speedtest.sjc01.softlayer.com/speedtest/speedtest/random500x500.jpg' ,
                 'tokyo': 'http://speedtest.tokyo.linode.com/100MB-tokyo.bin',
                 'use': 'http://speedtest.newark.linode.com/100MB-newark.bin',
                 'usw': 'http://speedtest.fremont.linode.com/100MB-fremont.bin',
                 'washington': 'http://speedtest.wdc01.softlayer.com/downloads/test500.zip'
                 }
    overall_time_elapsed = 0
    __size = 0

    def get_filesize(self):
        return self.__size

    def get_location(self, location=None):
        if location is None:
            location = self.DEFAULT_LOCATION
        return self.locations.get(location)

    def get_local_filename(self, url):
        return url.split('/')[-1]

    def download_file(self, url) :
      self.localFilename = self.get_local_filename(url)
      with open('/tmp/' + self.localFilename, 'wb') as f:
        self.__size = 0
        dl_speed = 0
        #start = time.clock()
        start = time.mktime(time.localtime())
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')

        if total_length is None: # no content length header
          f.write(r.content)
        else:
          for chunk in r.iter_content(1024):
            self.__size += len(chunk)
            f.write(chunk)
            done = int(50 * self.__size / int(total_length))
            #time_elapsed = (time.clock() - start)
            time_elapsed = (time.mktime(time.localtime()) - start)
            if time_elapsed > 0:
                dl_speed = self.__size/time_elapsed
                self.overall_time_elapsed = time_elapsed

            if self.VERBOSE:
              #Convert to MB/s and Mbps for printing
              sys.stdout.write("\r[%s%s] %s MB/s - %s Mbps" % ('=' * done, ' ' * (50-done), round(dl_speed*0.000001,2), round(dl_speed*0.000008,2)))
              sys.stdout.flush()

          self.cleanup()
      return dl_speed

    def cleanup(self):
      #Cleanup
      os.remove("/tmp/" + self.localFilename)
