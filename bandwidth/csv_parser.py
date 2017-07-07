#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

import csv
import statistics
import time

def csv_parser(results, csv_file):
    overall_speeds = ()
    with open(csv_file, 'wb') as myfile:
        wr = csv.writer(myfile)
        #TODO: Add date of test and test info to file
        date = ["Date", time.strftime("%c")]
        wr.writerow(date)
        wr.writerow([])
        overall_speeds = calculate_overall_speed(results)
        median_speeds = statistics.median(results)
        overall_header = ["Average (MB/s)", "Average (Mbps)", "Median (MB/sec)", "Median (Mbps)"]
        overall_speeds_csv = [overall_speeds[0], overall_speeds[1], round(median_speeds[0],2), round(median_speeds[1],2)]
        wr.writerow(overall_header)
        wr.writerow(overall_speeds_csv)
        wr.writerow([])
        #host_info = ["FTP Server", self.__]
        header = ["Sample#", "File Size", "Average Speed (MB/sec)", "Average Throughput (Mbps)"]
        wr.writerow(header)
        n = 1
        for result in results:
            #convert file size to MB
            size = round(result[3]/1024/1024,2)
            row = [n,size,round(result[0],2),round(result[1],2)]
            wr.writerow(row)
            n += 1

def calculate_overall_speed(results):
    overall_avg_speed = 0
    overall_avg_speed_mbps = 0
    n = 0
    for result in results:
        overall_avg_speed += round(result[0],2)
        overall_avg_speed_mbps += round(result[1],2)
        n += 1

    return (overall_avg_speed,overall_avg_speed_mbps)
