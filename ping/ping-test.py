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
VERBOSE = True

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
    parser.add_argument(
        "-s", "--silent", action="store_true", help="Don't print verbose output from the test")


    return parser.parse_args()

def signal_handler(signal, frame):
        print ('\n\nTest cancelled!\n')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    global VERBOSE
    options = parse_option()
    if options.silent:
        VERBOSE = False
    verboseprint = print if VERBOSE else lambda *a, **k: None

    transmitter = pingparsing.PingTransmitter()
    transmitter.interface = options.interface
    #transmitter.waittime = 10
    transmitter.count = options.count or DEFAULT_PING_COUNT
    ping_results = []

    scriptDir = sys.path[0]
    hosts = os.path.join(scriptDir, options.pingfile)
    hostsFile = open(hosts, "r")
    lines = hostsFile.readlines()
    if transmitter.interface is None:
        verboseprint("Network Interface: Default")
    else:
        verboseprint("Network Interface: " + str(transmitter.interface))
    verboseprint("\nPing Count: " + str(transmitter.count))
    verboseprint("\nTotal Tests: " + str(file_len(options.pingfile)) + "\n")
    n = 0
    for line in lines:
        if not line.startswith("#"):
            verboseprint ("Test #" + str(n + 1) + ": ")
            line = line.strip()
            verboseprint("Pinging Host " + line)
            transmitter.destination_host = line
            result = transmitter.ping()
            ping_parser = pingparsing.PingParsing()
            try:
                ping_parser.parse(result)
                host = [line,ping_parser]
                ping_results.append(host)
                verboseprint("PLC: {0} PLR: {1}% RTT_MIN: {2}ms RTT_MAX: {3}ms RTT_AVG: {4}ms\n".format(ping_parser.packet_loss_count,ping_parser.packet_loss_rate,ping_parser.rtt_min,ping_parser.rtt_max,ping_parser.rtt_avg))
            except AttributeError as e:
                verboseprint("Non-existent Host: " + line + "\n")
                #logger.debug(e)
            #verboseprint("Results:")
            n += 1

    csv_file = os.path.join(scriptDir, options.outfile)
    ping_parsers.csv_ping_parser(ping_results,csv_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())
