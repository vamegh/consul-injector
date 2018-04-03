#!/bin/bash
#
##
##########################################################################
#                                                                        #
#       consul-injector :: setup                                         #
#                                                                        #
#       (c) 2018 Vamegh Hedayati                                         #
#                                                                        #
#       Vamegh Hedayati <gh_vhedayati AT ev9 DOT io>                     #
#                                                                        #
#       Please see Copying for License Information                       #
#                             GNU/LGPL                                   #
##########################################################################
##
#

if [ $HOME = "/root" ]; then
  echo "please dont run me as root or run this script using sudo -H ..."
  exit 1
fi

sudo -H pip install virtualenv
sudo rm -rf build/
sudo rm -rf dist/
sudo rm -rf consul_injector.egg-info
sudo python3 setup.py install
sudo rm -rf build/
sudo rm -rf dist/
sudo rm -rf consul_injector.egg-info

