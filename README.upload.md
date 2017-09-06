# Bandwidth Measurement

## Upload Speed Test

Measure the upload speed by uploading a file to an FTP server. Optionally with the `-c` parameter the test can be run multiple times and calculate the average upload speed, and save the results to a file with CSV format (`-o` parameter).

### Required Python Modules

- numpy
- statistics

### usage

```
usage: upload-tester [-h] [-c COUNT] -f UPLOADFILE [-o OUTFILE] [-s] -l HOST
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

### Examples

```
python upload-tester -f /path/to/file -l ftp.myserver.com -u ftpuser -p ftppassword

```

Enable passive mode:

```
python upload-tester -f /path/to/file -l ftp.myserver.com -u ftpuser -p ftppassword -P

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
