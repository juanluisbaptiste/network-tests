# !/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

from __future__ import print_function
import csv
import numpy
import time


def csv_ping_parser(results, csv_file, overall_values):
    with open(csv_file, 'wb') as myfile:
        wr = csv.writer(myfile)
        date = time.strftime("%c")
        overall_headers = ["Count",
                           "Time Elapsed (s)",
                           "Min (ms)",
                           "Max (ms)",
                           "Average (ms)",
                           "Packet Loss Count",
                           "Packet Loss Rate (%)",
                           "Standard Deviation (ms)",
                           "Program Version"]
        wr.writerow(overall_headers)
        wr.writerow(overall_values)
        wr.writerow([])
        header = ["Count",
                  "Min (ms)",
                  "Max (ms)",
                  "Average (ms)",
                  "Std Deviation (ms)",
                  "Lost",
                  "% Lost",
                  "Host"]
        wr.writerow(header)
        for result in results:
            row = [result[1].packet_transmit,
                   result[1].rtt_min,
                   result[1].rtt_max,
                   result[1].rtt_avg,
                   numpy.std(result[1].rtt_avg),
                   result[1].packet_loss_count,
                   result[1].packet_loss_rate,
                   result[0]]
            wr.writerow(row)


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


def calculate_overall_values(results):
    overall_avg_speed = 0
    overall_avg_speed_mbps = 0
    n = 0
    for result in results:
        overall_avg_speed += round(result[0], 2)
        overall_avg_speed_mbps += round(result[1], 2)
        n += 1

    return (overall_avg_speed, overall_avg_speed_mbps)
