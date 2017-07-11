#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

from __future__ import print_function

import argparse
import numpy
import os
import signal
import sys
import time

import pingparsing
import ping_parsers

DEFAULT_PING_COUNT = 5
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

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def signal_handler(signal, frame):
        print ("\n\nTest cancelled!\n")
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def get_min_avg(results):
    return get_avg(results,'rtt_min')

def get_max_avg(results):
    return get_avg(results,'rtt_max')

def get_ping_avg(results):
    return get_avg(results,'rtt_avg')

def get_packetlostcount_avg(results):
    return get_avg(results,'packet_loss_count')

def get_packetlostrate_avg(results):
    return get_avg(results,'packet_loss_rate')

def get_avg(results,metric):
    val = 0
    for result in results:
        val += getattr(result[1],metric)
    return round(val/len(results),2)

def get_std_deviation(results):
    vals = []
    for result in results:
        vals.append(result[1].rtt_avg)
    return round(numpy.std(vals)/len(results),2)


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
        verboseprint("\nNetwork Interface: " + str(transmitter.interface))
    verboseprint("Ping Count: " + str(transmitter.count))
    verboseprint("Hosts: " + str(file_len(options.pingfile)) + "\n")

    start = time.mktime(time.localtime())
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
                ping_result = [line,ping_parser]
                ping_results.append(ping_result)
                verboseprint("Min: {0} ms Max: {1} ms Average: {2} ms Packet Loss Count: {3} Packet Loss Rate: {4}%\n".format(ping_parser.rtt_min,ping_parser.rtt_max,ping_parser.rtt_avg,ping_parser.packet_loss_count,ping_parser.packet_loss_rate))
            except AttributeError as e:
                verboseprint("Non-existent Host: " + line + "\n")
            n += 1
    time_elapsed = (time.mktime(time.localtime()) - start)
    verboseprint("\nTime elapsed: " + str(time_elapsed) + " seconds")
    #Calculate stats
    avg_min = get_min_avg(ping_results)
    avg_max = get_max_avg(ping_results)
    avg_ping = get_ping_avg(ping_results)
    avg_plc = get_packetlostcount_avg(ping_results)
    avg_plr = get_packetlostrate_avg(ping_results)
    std_deviation = get_std_deviation(ping_results)
    overall = (options.count,avg_min,avg_max,avg_ping,avg_plc,avg_plr,std_deviation)
    verboseprint("\nAverage min: " + str(avg_min) + " ms")
    verboseprint("Average max: " + str(avg_max) + " ms")
    verboseprint("Average ping: " + str(avg_ping) + " ms")
    verboseprint("Average packet loss count: " + str(avg_plc))
    verboseprint("Average packet loss rate: " + str(avg_plr) + " %")
    verboseprint("Standard deviation: " + str(std_deviation) + " ms\n")

    if options.outfile:
        csv_file = os.path.join(scriptDir, options.outfile)
        ping_parsers.csv_ping_parser(ping_results,csv_file,overall)

    return 0


if __name__ == "__main__":
    sys.exit(main())
