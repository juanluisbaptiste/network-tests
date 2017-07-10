# Latency Measurement

This script has the following feautures:

## Features
- Run multiple tests in one go.
- Calculate average speeds for multiple tests.
- Speed measurement in both Mbps and MB/s
- Save the results to a file with CSV format.
- Toggle FTP passive mode.

## Required Python Modules
- pingparsing

### Usage

```
usage: ping-test.py [-h] [-c COUNT] -f PINGFILE -o OUTFILE [-I INTERFACE]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Ping count. Default: 20
  -f PINGFILE, --pingfile PINGFILE
                        List of hosts to ping
  -o OUTFILE, --outfile OUTFILE
                        Destination file for ping results
  -I INTERFACE          Network interface to use for pinging
```

#### Examples

Run with no arguments and use default download location:

```
python ping-test.py -f hosts.txt
```

Save results to a CSV file:

```
python ping-test.py -f hosts.txt -o results.csv
```

Sample CSV output:

```
Date,Fri Jul  7 02:48:54 2017

Count,Lost,% Lost,Min,Max,Average,Host
5,0,0.0,12.638,21.849,16.211,www.cisco.com
5,0,0.0,12.013,15.859,13.801,www.google.com
5,0,0.0,12.422,15.944,13.913,www.adobe.com
5,0,0.0,78.372,82.801,80.783,www.hotmail.com
5,0,0.0,53.662,57.935,56.27,www.akamai.com

```
