#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

import errno
from socket import error as SocketError
import ftplib
import ntpath
import os
import sys
import time

import common


class UploadTester():
    DEFAULT_UPLOAD_COUNT = 1
    VERBOSE = True
    host = ""
    username = ""
    password = ""
    passive = False
    current_dir = "/"
    overall_time_elapsed = 0

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

    def upload_file(self, upload_file):
        chunk_size = 8192
        dl_speed = 0
        global n
        self.__sizeWritten = 0

        self.__ftp.connect(self.host, 21)
        try:
            self.__ftp.login(self.username, self.password)
        except ftplib.error_perm, e:
            if "530 Login authentication failed" in e:
                print "ERROR: Bad username or password."
                print
                sys.exit(1)
        # Set passive mode
        self.__ftp.set_pasv(self.passive)
        self.__ftp.cwd(self.current_dir)
        self.__filesize = os.path.getsize(upload_file)
        # self.__start = time.clock()
        self.__start = time.mktime(time.localtime())
        file = open(upload_file, 'rb')
        self.__filename = ntpath.basename(upload_file)
        try:
            self.__ftp.storbinary('STOR ' + self.__filename, file, chunk_size,
                                  self.print_progress)
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise  # Not error we are looking for
            # pass
            print "ERROR: Got connection reset, retring upload..."
            n = n + 1
        time_elapsed = (time.mktime(time.localtime()) - self.__start)
        self.overall_time_elapsed = time_elapsed
        dl_speed = self.__filesize/time_elapsed
        return dl_speed

    def print_progress(self, chunk):
        self.__sizeWritten += len(chunk)
        done = int(50 * self.__sizeWritten / int(self.__filesize))
        time_elapsed = (time.mktime(time.localtime()) - self.__start)
        try:
            dl_speed = self.__sizeWritten/time_elapsed
            avr_speed = (dl_speed)/1000000
            avr_speed_mbps = (dl_speed)*common.SPEED_MBIT_SEC
            if self.VERBOSE:
                sys.stdout.write("\r[%s%s] %s MB/s - %s Mbps" %
                                 ('=' * done, ' ' * (50-done),
                                  round(avr_speed, 2),
                                  round(avr_speed_mbps, 2)))
                sys.stdout.flush()
        except ZeroDivisionError:
            pass
