# bandwidth Measurement

Both scripts have the following feautures:

## Features
- Run multiple tests in one go.
- Calculate average speeds for multiple tests.
- Speed measurement in both Mbps and MB/s
- Save the results to a file with CSV format.

### Download Speed Test

Measure the download speed by downloading an HTTP test file from a predefined list of locations or specify your own using the `-u` parameter (it must be an HTTP url). The script only supports HTTP url's. Optionally with the `-c` parameter the test can be run multiple times and calculate the average download speed, and save the results to a file with CSV format (`-o` parameter).

#### Required Python Modules

- numpy
- requests
- statistics

### Usage

```
usage: download-speed.py [-h] [-c COUNT]
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

#### Examples

Run with no arguments and use default download location:

```
python download-speed.py
```

Use custom download url:

```
python download-speed.py -u http://yourserver.com/file.zip
```

Save results to a CSV file:

```
python download-speed.py -o results.csv
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


### Upload Speed Test

Measure the upload speed by uploading a file to an FTP server. Optionally with the `-c` parameter the test can be run multiple times and calculate the average upload speed, and save the results to a file with CSV format (`-o` parameter).

#### Required Python Modules

- numpy
- statistics

### usage

```
usage: upload-speed.py [-h] [-c COUNT] -f UPLOADFILE [-o OUTFILE] [-s] -l HOST
                       -u USERNAME -p PASSWORD [-P PASSIVE]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of uploads to do. Default: 1
  -f UPLOADFILE, --uploadfile UPLOADFILE
                        Test file to upload
  -o OUTFILE, --outfile OUTFILE
                        Destination file for test results in CSV format
  -s, --silent          Don't print verbose output from the upload process
  -l HOST, --host HOST  FTP server for upload test
  -u USERNAME, --username USERNAME
                        FTP user name for upload test
  -p PASSWORD, --password PASSWORD
                        FTP password for upload test
  -P PASSIVE, --passive PASSIVE
                        Sets FTP passive mode. Default: False
```

#### Examples

```
python upload-speed.py -f /path/to/file -l ftp.myserver.com -u ftpuser -p ftppassword

```

Enable passive mode:

```
python upload-speed.py -f /path/to/file -l ftp.myserver.com -u ftpuser -p ftppassword -P

```

Sample CSV output:

```
Date,Server,File,Size,Min (MB/s),Min (Mbps),Max (MB/s),Max (Mbps),Average (MB/s),Average (Mbps),Median (MB/sec),Median (Mbps)
Mon Jul 10 00:11:00 2017,ftp.server.yyy,/home/juancho/Downloads/Test.zip,4.16,0.15,0.15,0.23,1.84,0.18,1.42,0.17,1.34

Sample#,File Size,Average Speed (MB/sec),Average Throughput (Mbps)
1,4.16,0.17,1.34
2,4.16,0.15,1.2
3,4.16,0.23,1.84
4,4.16,0.17,1.34
5,4.16,0.17,1.4

```
