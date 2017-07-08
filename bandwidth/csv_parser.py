#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

import csv

def csv_parser(results, csv_file, overall, filesize):
    overall_speeds = ()
    with open(csv_file, 'wb') as myfile:
        wr = csv.writer(myfile)
        #TODO: Add date of test and test info to file
        overall_header = overall[0]
        overall_speeds_csv = overall[1]
        wr.writerow(overall_header)
        wr.writerow(overall_speeds_csv)
        wr.writerow([])
        header = ["Sample#", "File Size", "Average Speed (MB/sec)", "Average Throughput (Mbps)"]
        wr.writerow(header)
        n = 1
        for result in results:
            row = [n,filesize,round(result*0.000001,2),round(result*0.000008,2)]
            wr.writerow(row)
            n += 1

def calculate_overall_speed(results):
    overall_avg_speed = 0
    n = 0
    for result in results:
        overall_avg_speed += round(result,2)
        n += 1

    return overall_avg_speed/n
