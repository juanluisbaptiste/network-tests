#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

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
            self.__ftp.delete(self.__filename)
            self.__ftp.quit()
        except (ftplib.error_temp, ftplib.error_perm, ftplib.error_reply):
            pass
        self.__ftp.close()

    def upload_file(self, upload_file) :
        chunk_size = 8192
        dl_speed = 0
        self.__sizeWritten = 0

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
        #self.__start = time.clock()
        self.__start = time.mktime(time.localtime())
        file = open(upload_file, 'rb')
        self.__filename = ntpath.basename(upload_file)
        #Sleep one second to guarantee there's a time difference
        self.__ftp.storbinary('STOR ' + self.__filename, file, chunk_size, self.print_progress)
        time_elapsed = (time.mktime(time.localtime()) - self.__start)
        dl_speed = self.__filesize/time_elapsed
        avr_speed = (dl_speed)/1000000
        avr_speed_mbps = (dl_speed)*0.000008
        results = (avr_speed,avr_speed_mbps,time_elapsed, float(self.__filesize))
        return results

    def print_progress(self,chunk):
        self.__sizeWritten += len(chunk)
        done = int(50 * self.__sizeWritten / int(self.__filesize))
        time_elapsed = (time.mktime(time.localtime()) - self.__start)
        try:
            dl_speed = self.__sizeWritten/time_elapsed
            avr_speed = (dl_speed)/1000000
            avr_speed_mbps = (dl_speed)*0.000008
            if self.VERBOSE:
                sys.stdout.write("\r[%s%s] %s MB/s - %s Mbps" % ('=' * done, ' ' * (50-done), round(avr_speed,2), round(avr_speed_mbps,2)))
                sys.stdout.flush()
        except ZeroDivisionError:
            pass
