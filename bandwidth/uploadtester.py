#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

import csv
import datetime
import ftplib
import ntpath
import os
import sys
import time

class UploadTester():
    DEFAULT_UPLOAD_COUNT = 1
    VERBOSE = False
    host = ""
    username = ""
    password = ""
    passive = False

    __sizeWritten = 0
    __filesize = 0
    __filename = ""
    __start = 0
    __ftp = ftplib.FTP()

    def cleanup(self):
        try:
            self.__ftp.quit()
        except ftplib.error_temp, ftplib.error_reply:
            pass
        self.__ftp.close()

    def upload_file(self, upload_file) :
        chunk_size = 8192
        dl_speed = 0

        self.__ftp.connect(self.host,21)
        try:
            self.__ftp.login(self.username, self.password)
        except ftplib.error_perm,e:
            if "530 Login authentication failed" in e:
                print "ERROR: Bad username or password."
                print
                sys.exit(1)
        #Set passive mode
        self.__ftp.set_pasv(self.passive)
        self.__filesize = os.path.getsize(upload_file)
        dl_speed = 0
        self.__start = time.clock()
        file = open(upload_file, 'rb')
        filename = ntpath.basename(upload_file)
        self.__ftp.storbinary('STOR ' + filename, file, 1024, self.print_progress)
        time_elapsed = (time.clock() - self.__start)
        dl_speed = self.__filesize/time_elapsed
        avr_speed = (dl_speed)/800000000
        avr_speed_mbps = (dl_speed)/100000000
        results = (avr_speed,time_elapsed, self.__filesize)
        self.cleanup()
        return results

    def print_progress(self,chunk):
        self.__sizeWritten += len(chunk)

        done = int(50 * self.__sizeWritten / int(self.__filesize))
        time_elapsed = (time.clock() - self.__start)
        dl_speed = self.__filesize/time_elapsed
        avr_speed = (dl_speed)/800000000
        avr_speed_mbps = (dl_speed)/100000000

        if self.VERBOSE:
            sys.stdout.write("\r[%s%s] %s MB/s - %s Mbps" % ('=' * done, ' ' * (50-done), round(avr_speed,2), round(avr_speed_mbps,2)))
            sys.stdout.flush()

    def csv_parser(self, results, csv_file):
        with open(csv_file, 'wb') as myfile:
            wr = csv.writer(myfile)
            #TODO: Add date of test and test info to file
            header = ["Sample#", "File Size", "Average Speed (MB/sec)", "Average Throughput (Mbps)"]
            wr.writerow(header)
            n = 1
            for result in results:
                row = [n,result[2],round(result[0])]
                wr.writerow(row)
                n += 1
