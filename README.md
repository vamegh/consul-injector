# consul-injector
A simple Python Utility to inject KV pairs into Consul, Useful for Automation

# consul-extractor
A simple Python Utility to extractt KV pairs from Consul, Useful for Automation

## Introduction:
This little utility is designed to allow quick population of newly installed consul servers - it serves as a method to repopulate consul servers or to add new KV data or to extract KV data.
It now supports both json and yaml data files, they can both be supplied at runtime using the -d command line flag, or specified via command line options. It supports extracting in either format using the -f or format command line flag.

## Testing
A simple docker-compose is provided in the docker/ directory, first steps:

```
  cd docker
  docker-compose up -d
```

This should bring up the docker containers, open a browser go to http://1227.0.0.1:8500
The Consul ui should be present the acl_token is l3tm31n.

next run setup.sh this should setup everything necessary to make this tool work. It will also be necessary to run the following:

```
sudo mkdir /var/log/consul-injector
sudo -s chown ${SUDO_USER}:${SUDO_USER} /var/log/consul-injector
```

This has been tested on python3.6 and python2.7 on ubuntu 17.10 and should support python2.7+ and python3.x
It defaults to system python, if you wish to use an explicit python version please modify bin/consul-injector and modify the setup.sh.

if you don't wish to install this package using the setup.py method, it can be run manually, for manual installation please do the following:

```
cd consul-injector
sudo mkdir /etc/consul-injector
sudo cp -rpfv configs/* /etc/consul-injector/
sudo mkdir /var/log/consul-injector
sudo -s chown ${SUDO_USER}:${SUDO_USER} /var/log/consul-injector
cp bin/* .
./consul-injector
## To test extraction of the testing k/v data
./consul-extractor -q testing -r -f json -o /tmp/testing.json
```

This should make and sort out all of the various dependencies, please note the configs are read from /etc/consul-injector this can be modified by modifying configs/config.yaml or specifying the correct command line flag.


##Supported Options:

```
$ ./consul-injector --help
Usage: consul-injector [options]
Version: 0.1.5

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -c CONFIG, --config=CONFIG
                        Provide a custom configuration file, defaults to /etc
                        /consul-injector/config.yaml if none provided
  -d DATA_FILE, --data_file=DATA_FILE
                        Provide data files to import (optional) this can be
                        called multiple times to import multiple files, This
                        is the data to import into consul example: -D
                        <path>/data1.yaml -D <path>/data2.json -D
                        <path>/data3.yaml etc.
  --force               Force running script (if you must run as root)- use
                        with care
  -D DEBUG, --debug=DEBUG
                        set debugging level:  an integer value between 1 to 5
                        (the higher the more debugging output that will be
                        provided)
  -H HOST, --host=HOST  add a custom login host defaults to localhost
  -t TOKEN, --token=TOKEN
                        add a custom consul acl token (optional)
  -p PORT, --port=PORT  add a custom consul port defaults to 8500
  --sslverify           enable ssl verification (defaults to False)
```

```
$ ./consul-extractor --help
Usage: consul-extractor [options]
Version: 0.1.5

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -c CONFIG, --config=CONFIG
                        Provide a custom configuration file, defaults to /etc
                        /consul-injector/config.yaml if none provided
  -d DATA_FILE, --data_file=DATA_FILE
                        Provide data files to import (optional) this can be
                        called multiple times to import multiple files, This
                        is the data to import into consul example: -D
                        <path>/data1.yaml -D <path>/data2.json -D
                        <path>/data3.yaml etc.
  --force               Force running script (if you must run as root)- use
                        with care
  -D DEBUG, --debug=DEBUG
                        set debugging level:  an integer value between 1 to 5
                        (the higher the more debugging output that will be
                        provided)
  -H HOST, --host=HOST  add a custom login host defaults to localhost
  -t TOKEN, --token=TOKEN
                        add a custom consul acl token (optional)
  -p PORT, --port=PORT  add a custom consul port defaults to 8500
  --sslverify           enable ssl verification (defaults to False)
  -q QUERY, --query=QUERY
                        add a query to gather information from consul
                        (required)
  -o OUTFILE, --outfile=OUTFILE
                        specify the output path and file - default:
                        /tmp/consul_extractor_data.json
  -f FORMAT, --format=FORMAT
                        specify the output format (json or yaml)
  -r, --recurse         enables recursive querying (defaults to False)
```

## Feedback
If you have any feedback any issues, please let me know, if you have any changes or want to submit any patches or fixes feel free.
I hope to add aws support to make the configs available in an s3 bucket to allow for easy deployment and updates in aws, also git support for pulling and pushing the configs
will hopefully be added some time soon - which will allow for easy backing up of the config files.

