# network-tests
Collection of python scripts to do multiple network tests like download/upload speeds and network 
latency (ping). It also calculates statistics like averages, medians, min and max values and store 
results in a CSV file.

The scripts have the following features:

## Features
- Run multiple tests in one go.
- Calculate average speeds for multiple tests.
- For bandwidth measurement in both Mbps and MB/s.
- Overall statistics with metrics like minimum, maximum and average speeds, and standard deviation.
- Save the results to a file with CSV format.
- Docker image that includes all the scripts and dependencies.
- Automated periodic test runs.
- Send csv results by email.

## Included scripts

See the other README files for examples and usage instructions.

### Measure Latency
#### [ping-tester](https://github.com/juanluisbaptiste/network-tests/tree/master/README.ping.md)


Script for doing ping tests to a list of sites on a file and optionally save results on a csv file.

### Measure Bandwidth

#### [download-tester](https://github.com/juanluisbaptiste/network-tests/tree/master/README.download.md)


Script for doing download speed tests and optionally save results on a csv file.

#### [upload-tester](https://github.com/juanluisbaptiste/network-tests/tree/master/README.upload.md)


Script for doing upload speed tests and optionally save results on a csv file.

## Installation

    git clone https://github.com/juanluisbaptiste/network-tests.git
    cd network-tests
    sudo python setup.py install

## Usage

See each script README file for detailed instructions.

## Docker image
There is a docker image available to run the scripts. The tests scripts to run can
be driven by the following environment variables (refer to each test program for
  the usage description of each variable):

To enable each of the tests (these are also the defaults):
* DOWNLOAD_TEST_ENABLE=yes
* UPLOAD_TEST_ENABLE=no
* PING_TEST_ENABLE=no

Download test configuration:
* DOWNLOAD_TEST_COUNT=1
* DOWNLOAD_TEST_LOCATION=
* DOWNLOAD_TEST_OUTFILE=
* DOWNLOAD_TEST_SILENT=no
* DOWNLOAD_TEST_URL=

Upload test configuration:
* UPLOAD_TEST_COUNT=1
* UPLOAD_TEST_FILE=
* UPLOAD_TEST_OUTFILE=
* UPLOAD_TEST_SILENT=no
* UPLOAD_TEST_HOST=
* UPLOAD_TEST_USER=
* UPLOAD_TEST_PASSWORD=
* UPLOAD_TEST_PASSIVE=no

Ping test configuration:
* PING_TEST_COUNT=1
* PING_TEST_FILE=
* PING_TEST_OUTFILE=
* PING_TEST_INTERFACE=Default
* PING_TEST_SILENT=no

Global options:
* SILENT_TEST: Disable output in all tests being run.

There's an example [env file](https://github.com/juanluisbaptiste/network-tests/blob/master/.env.example) you can use with the included [docker-compose file](https://github.com/juanluisbaptiste/network-tests/blob/master/docker-compose.yml).

### Automated tests configuration:

Test execution can be automated:

* CRON_EXPRESSION: If a cron expression is set then automated reports will be run at the specified time. This is the default. For example, the following setting will run the tests the first day of each month past midnight:

      CRON_EXPRESSION="5 0 1 \* \*"

Allo those environment variables are passed to a script called _/run_test.sh_, which you can also call from outside the container if you want to do a manual run instead:

    sudo docker-compose tests /run_test.sh

And the tests will be run as configured on the .env file.

### Bandwidth Throttling

It also includes [throttle](https://www.sitespeed.io/documentation/throttle/), so different network conditions can be emulated while testing. To launch it:

    sudo modprobe ifb numifbs=1
    sudo docker pull juanluisbaptiste/network-tests
    sudo docker run -ti --cap-add NET_ADMIN --name network-tests juanluisbaptiste/network-tests bash

These environment variables controls bandwidth throttling:
* THROTTLE_ENABLE=no
* THROTTLE_PROFILE= (see [throttle](https://www.sitespeed.io/documentation/throttle/) documentation for possible values)
* THROTTLE_DOWN_SPEED=
* THROTTLE_UP_SPEED=
* THROTTLE_RTT=1

If you are not using the docker image, before running the tests enable throttle with the desired network speed configuration:

throttle --profile 3g

See throttle's documentation for details on how to use it. when you finish testing you can disable it:

throttle --stop

### Results by email

If you want the csv file to be sent to you be email then configure these environment variables:
* SEND_RESULTS_EMAIL=yes
* SMTP_FROM=from@email.com
* SMTP_TO=destination@email.com
