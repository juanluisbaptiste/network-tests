#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

from __future__ import print_function

import argparse
import os
import signal
import sys
import pingparsing
import ping_parsers

DEFAULT_PING_COUNT = 20


def parse_option():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--count", required=False, help="Ping count. Default: " + str(DEFAULT_PING_COUNT))
    parser.add_argument(
        "-f", "--pingfile", required=True, help="List of hosts to ping")
    parser.add_argument(
        "-o", "--outfile", required=False, help="Destination file for ping results")
    parser.add_argument(
        "-I", dest="interface", help="Network interface to use for pinging")

    return parser.parse_args()

def signal_handler(signal, frame):
        print ('\n\nTest cancelled!\n')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    options = parse_option()
    transmitter = pingparsing.PingTransmitter()
    transmitter.interface = options.interface
    #transmitter.waittime = 10
    transmitter.count = options.count or DEFAULT_PING_COUNT
    ping_results = []

    scriptDir = sys.path[0]
    hosts = os.path.join(scriptDir, options.pingfile)
    hostsFile = open(hosts, "r")
    lines = hostsFile.readlines()

    for line in lines:
        if not line.startswith("#"):
            line = line.strip()
            transmitter.destination_host = line
            result = transmitter.ping()
            ping_parser = pingparsing.PingParsing()
            try:
                ping_parser.parse(result)
                host = [line,ping_parser]
                ping_results.append(host)
            except AttributeError as e:
                print ("Non-existent Host: " + line)
                print ()
                #logger.debug(e)

    csv_file = os.path.join(scriptDir, options.outfile)
    ping_parsers.csv_ping_parser(ping_results,csv_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
