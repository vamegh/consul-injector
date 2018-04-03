# consul-injector
A simple Python Utility to inject KV pairs into Consul, Useful for Automation

## Introduction:
This little utility is designed to allow quick population of newly installed consul servers - it serves as a method to repopulate consul servers or to add new KV data.

## Usage
A simple docker-compose is provided in the docker/ directory, first steps:

```
  cd docker
  docker-compose up -d
```

This should bring up the docker containers, open a browser go to http://1227.0.0.1:8500
The Consul ui should be present the acl_token is l3tm31n.

next run setup.sh this should setup everything necessary to make this tool work, it is built using python3.6 on ubuntu 17.10.
This should also work fine on python2.7 (originally python2.7 was used and then quickly switched to python3.6)
if using a different python version please modify bin/consul-injector and modify the setup.sh.

if you dont wish to install this package using the setup.py method, it can be run manually, for manual installation please do the following:

```
cd consul-injector
sudo mkdir /etc/consul-injector
sudo cp -rpfv configs/* /etc/consul-injector/
sudo mkdir /var/log/consul-injector
sudo -s chown ${SUDO_USER}:${SUDO_USER} /var/log/consul-injector
cp bin/consul-injector .
./consul-injector
```

This should make and sort out all of the various dependencies, please note the configs are read from /etc/consul-injector this can be modified by modifying configs/config.yaml


## Feedback
If you have any feedback any issues, please let me know, if you have any changes or want to submit any patches or fixes feel free.
I hope to add aws support to make the configs available in an s3 bucket to allow for easy deployment and updates in aws, also git support for pulling and pushing the configs
will hopefully be added some time soon - which will allow for easy backing up of the config files.

