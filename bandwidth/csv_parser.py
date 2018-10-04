#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Juan Luis Baptiste <juan.baptiste@gmail.com>
"""

import csv


def csv_parser(results, csv_file, overall, filesize):
    """Create csv file from test results.

    Arguments:
    results -- Array with the test results
    csv_file --  Destination csv file
    overall -- Array with overall test data (averages, deviations, etc)
    filesize -- Size of the file being uploaded/downloaded
    """
    with open(csv_file, 'wb') as myfile:
        wr = csv.writer(myfile)
        # TODO: Add date of test and test info to file
        overall_header = overall[0]
        overall_speeds_csv = overall[1]
        wr.writerow(overall_header)
        wr.writerow(overall_speeds_csv)
        wr.writerow([])
        header = ["Sample#",
                  "File Size",
                  "Average Speed (MB/sec)",
                  "Average Throughput (Mbps)"]
        wr.writerow(header)
        n = 1
        for result in results:
            row = [n,
                   filesize,
                   round(result*0.000001, 2),
                   round(result*0.000008, 2)]
            wr.writerow(row)
            n += 1
