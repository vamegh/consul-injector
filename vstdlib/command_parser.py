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
                               help='Provide a custom configuration file, defaults to /etc/consul-injector/config.yaml if none provided')
        self.parser.add_option('--force', action='store_true',
                               dest='force', default=False,
                               help='Force running script (if you must run as root)- use with care')

    def add_git(self):
        self.parser.add_option('-b', '--branch', action='store', default=None,
                               help='Provide a custom git branch to use, defaults to branch specified in config file or master if none provided')

    def add_debug(self):
        self.parser.add_option('-d', '--debug', action='store', type='int', default=None,
                               help='set debugging level (an integer value the higher the more debugging output that will be provided)')

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
        return config_data

    def debug(self):
        # type: () -> object
        if self.options.debug:
            print ("Setting modifying log level to match debug level")