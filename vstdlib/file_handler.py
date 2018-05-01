#
##
##########################################################################
#                                                                        #
#       consul-injector :: file_handler                                  #
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
import sys
import yaml
import json
import logging

def write_yaml(outfile=None, data=None):
    if not outfile or not data:
        logging.error("Error Data / Outfile Not Provided")
        sys.exit(1)
    with open(outfile, 'w') as outfile:
        outfile.write(yaml.safe_dump(data, default_flow_style=False,
                                     allow_unicode = True, encoding=None,
                                     explicit_start=True))

def write_json(outfile=None, data=None):
    if not outfile or not data:
        logging.error("Error Data / Outfile Not Provided")
        sys.exit(1)
    with open(outfile, 'w') as outfile:
        json.dump(data, outfile, indent=4)

