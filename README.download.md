# Bandwidth Measurement

## Download Speed Test

Measure the download speed by downloading an HTTP test file from a predefined list of locations or specify your own using the `-u` parameter (it must be an HTTP url). The script only supports HTTP url's. Optionally with the `-c` parameter the test can be run multiple times and calculate the average download speed, and save the results to a file with CSV format (`-o` parameter).

### Required Python Modules

- numpy
- requests
- statistics

### Usage

```
usage: download-tester [-h] [-c COUNT]
                         [-l {usw,use,tokyo,washington,sanjose,london}]
                         [-o OUTFILE] [-s] [-u URL]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of downloads to do. Default: 1
  -l {usw,use,tokyo,washington,sanjose,london}, --location {usw,use,tokyo,washington,sanjose,london}
                        Server location for the test. Default: use
  -o OUTFILE, --outfile OUTFILE
                        Destination file for test results in CSV format
  -s, --silent          Don't print verbose output from the download process
  -u URL, --url URL     Alternate download URL (it must include path and
```

### Examples

Run with no arguments and use default download location:

```
python download-tester
```

Use custom download url:

```
python download-tester -u http://yourserver.com/file.zip
```

Save results to a CSV file:

```
python download-tester -o results.csv
```

Sample CSV output:

```
Date,URL,Size (MB),Min (MB/s),Min (Mbps),Max (MB/s),Max (Mbps),Average (MB/s),Average (Mbps),Median (MB/sec),Median (Mbps)
Mon Jul 10 00:14:59 2017,http://speedtest.tokyo.linode.com/100MB-tokyo.bin,100.0,1.29,1.29,1.33,10.62,1.31,1.31,1.31,10.49

Sample#,File Size,Average Speed (MB/sec),Average Throughput (Mbps)
1,100.0,1.31,10.49
2,100.0,1.31,10.49
3,100.0,1.29,10.36
4,100.0,1.31,10.49
5,100.0,1.33,10.62
```
