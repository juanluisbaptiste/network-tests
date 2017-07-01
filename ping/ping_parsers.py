#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

from __future__ import print_function
import csv
import json

def csv_ping_parser(results, csv_file):
    with open(csv_file, 'wb') as myfile:
        wr = csv.writer(myfile)
        header = ["Perdidos", "% Perdidos", "Minimo", "Maximo", "Promedio", "Host"]
        wr.writerow(header)
        for result in results:
            row = [result[1].packet_loss_count,result[1].packet_loss_rate,result[1].rtt_min,result[1].rtt_max,result[1].rtt_avg,result[0]]
            wr.writerow(row)
            print (result[0])
            print_ping_parser(result[1])

def print_ping_parser(ping_parser):
    print("packet_transmit: {:d} packets".format(ping_parser.packet_transmit))
    print("packet_receive: {:d} packets".format(ping_parser.packet_receive))
    print("packet_loss_rate: {:.1f} %".format(
        ping_parser.packet_loss_rate))
    print("packet_loss_count: {:d} packets".format(
        ping_parser.packet_loss_count))

    if ping_parser.packet_duplicate_rate:
        packet_duplicate_rate = "{:.1f} %".format(
            ping_parser.packet_duplicate_rate)
    else:
        packet_duplicate_rate = "NaN"
    print("packet_duplicate_rate: {:s}".format(packet_duplicate_rate))

    if ping_parser.packet_duplicate_count:
        packet_duplicate_count = "{:d} packets".format(
            ping_parser.packet_duplicate_count)
    else:
        packet_duplicate_count = "NaN"
    print("packet_duplicate_count: {:s}".format(packet_duplicate_count))

    print("rtt_min:", ping_parser.rtt_min)
    print("rtt_avg:", ping_parser.rtt_avg)
    print("rtt_max:", ping_parser.rtt_max)
    print("rtt_mdev:", ping_parser.rtt_mdev)
    print()
