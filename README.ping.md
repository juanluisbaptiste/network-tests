# Latency Measurement

This script has the following features:

## Features
- Run multiple tests in one go.
- Overall statistics.
- Save the results to a file with CSV format.

## Required Python Modules
- pingparsing

### Usage

```
usage: ping-tester [-h] [-c COUNT] -f PINGFILE [-o OUTFILE] [-I INTERFACE]
                    [-s]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Ping count. Default: 5
  -f PINGFILE, --pingfile PINGFILE
                        List of hosts to ping
  -o OUTFILE, --outfile OUTFILE
                        Destination file for ping results
  -I INTERFACE          Network interface to use for pinging
  -s, --silent          Don't print verbose output from the test
```

#### Examples

Run with no arguments and use default download location:

```
python ping-tester -f hosts.txt
```

Save results to a CSV file:

```
python ping-tester -f hosts.txt -o results.csv
```

Sample CSV output:

```
Date,Count,Time Elapsed (s),Min (ms),Max (ms),Average (ms),Packet Loss Count,Packet Loss Rate (%),Standard Deviation (ms),Program Version
Wed Apr 10 12:11:58 2019,3,9.0,47.01,64.42,57.26,0.0,0.0,7.62,v0.1.4.1

Count,Min (ms),Max (ms),Average (ms),Std Deviation (ms),Lost,% Lost,Host
3,13.677,16.063,15.231,1.104,0,0.0,www.cisco.com
3,79.889,91.102,84.81,4.691,0,0.0,www.google.com
3,12.979,61.173,42.389,21.062,0,0.0,www.adobe.com
3,81.488,89.324,86.615,3.627,0,0.0,www.hotmail.com

```
