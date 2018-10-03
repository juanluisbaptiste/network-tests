# network-tests
Collection of python scripts to do network tests like download/upload speeds, network latency (ping) and store results in a CSV file with some stats.

The scripts have the following features:

## Features
- Run multiple tests in one go.
- Calculate average speeds for multiple tests.
- For bandwidth measurement in both Mbps and MB/s.
- Overall statistics with metrics like minimum, maximum and average speeds, and standard deviation.
- Save the results to a file with CSV format.
- Docker image that includes all the scripts and dependencies.

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
There is a docker image available to run the scripts. It also includes [throttle](https://www.sitespeed.io/documentation/throttle/), so different network conditions can be emulated while testing. To launch it:

    sudo modprobe ifb numifbs=1
    sudo docker pull juanluisbaptiste/network-tests
    sudo docker run -ti --cap-add NET_ADMIN --name network-tests juanluisbaptiste/network-tests bash

Then, inside the container you can run any of the scripts as explained above. If you need to emulate different network conditions you can use [throttle](https://www.sitespeed.io/documentation/throttle/) for that.

Before running the tests enable throttle with the desired network speed configuration:

    throttle --profile 3g

See throttle's documentation for details on how to use it. when you finish testing you can disable it:

    throttle --stop
