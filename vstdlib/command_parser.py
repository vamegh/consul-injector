#
##
##########################################################################
#                                                                        #
#       consul-injector :: command_parser                                #
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

from optparse import OptionParser
import sys
import yaml

class Commands(object):
    def __init__(self, name='', version='0.0.1', message=''):
        self.name = name
        self.version = version
        self.message = message
        self.parser = OptionParser(version=self.version,
                                   usage='\n'.join([
                                       self.name + ' [options]',
                                       'Version: ' + self.version,
                                   ]))

    def add_config(self):
        self.parser.add_option('-c', '--config', action='store', default='/etc/consul-injector/config.yaml',
                               help=' '.join(['Provide a custom configuration file,',
                                              'defaults to /etc/consul-injector/config.yaml if none provided']))
        self.parser.add_option('-d', '--data_file', action='append', default=None,
                               help=' '.join(['Provide data files to import (optional)',
                                              'this can be called multiple times to import multiple files,',
                                              'This is the data to import into consul example:',
                                              '-D <path>/data1.yaml -D <path>/data2.json -D <path>/data3.yaml etc.']))
        self.parser.add_option('--force', action='store_true',
                               dest='force', default=False,
                               help='Force running script (if you must run as root)- use with care')

    def add_git(self):
        self.parser.add_option('-b', '--branch', action='store', default=None,
                               help=' '.join(['Provide a custom git branch to use, defaults to',
                                              'branch specified in config file or master if none provided']))

    def add_debug(self):
        self.parser.add_option('-D', '--debug', action='store', type='int', default=None,
                               help=' '.join(['set debugging level: ',
                                              'an integer value between 1 to 5 (the higher the more',
                                              'debugging output that will be provided)']))

    def add_consul(self):
        self.parser.add_option('-H', '--host', action='store', default=None,
                               help='add a custom login host defaults to localhost')
        self.parser.add_option('-t', '--token', action='store', default=None,
                               help='add a custom consul acl token (optional)')
        self.parser.add_option('-p', '--port', action='store', default=None,
                               help='add a custom consul port defaults to 8500')
        self.parser.add_option('--sslverify', action='store_true',
                               dest='sslverify', default=False,
                               help='enable ssl verification (defaults to False)')
    def add_query(self):
        self.parser.add_option('-q', '--query', action='store', default=None,
                               help='add a query to gather information from consul (required)')
        self.parser.add_option('-o', '--outfile', action='store', default=None,
                               help='specify the output path and file - default: /tmp/consul_extractor_data.json')
        self.parser.add_option('-f', '--format', action='store', default='json',
                               help='specify the output format (json or yaml)')
        self.parser.add_option('-r', '--recurse', action='store_true',
                               dest='recurse', default=False,
                               help='enables recursive querying (defaults to False)')


    def set_options(self):
        options, args = self.parser.parse_args()
        return options, args, self.parser

class CommandCheck(object):
    def __init__(self, options=None, parser=None):
        self.options = options
        self.parser = parser

    def config(self):
        '''check the default options'''
        if self.options.config:
            try:
                with open(self.options.config, "r") as configyml:
                    config_data = yaml.safe_load(configyml)
                    return config_data
            except IOError as e:
                print ("\nConfig File Issue: %s :: Error : %s\n" % (self.options.config, e[1]))
                self.parser.print_help()
                sys.exit(1)

    def debug(self):
        if self.options.debug:
            print("Setting log level to match debug level")

    def query(self):
        try:
            if not self.options.query:
                self.parser.error("Query is Required")
        except AttributeError:
            self.parser.error("Query is Required")

    def format(self):
        valid_formats = ['json', 'yaml']
        try:
          if self.options.format not in valid_formats:
              self.parser.error("Format must be either json or yaml")
        except AttributeError:
            self.options.format = 'json'




