#
##
##########################################################################
#                                                                        #
#       consul-injector :: config_parser                                 #
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
import copy
import getpass
import os.path
import re
import sys
import yaml

from sys import version_info
py2 = version_info[0] == 2

if py2:
    input = raw_input


class ConfigParse(object):
    def __init__(self, options=None, parser=None):
        self.options = options
        self.parser = parser

    def read_yaml(self, config_file=''):
        try:
            with open(config_file, "r") as config:
                yaml_data = yaml.safe_load(config)
            return yaml_data
        except IOError as e:
            print ("Error: %s :: skipping" % (str(e)))

    def combine_config(self, cfg_data=None):
        try:
            color_map = cfg_data['color_map']
            color_data = self.read_yaml(config_file=color_map)
            if color_data:
                cfg_data.update(color_data)
        except KeyError as err:
            print ("color map not supplied :: Error: %s :: skipping", err)
        try:
            git_config = cfg_data['git_config']
            git_data = self.read_yaml(config_file=git_config)
            if git_data:
                cfg_data.update(git_data)
        except KeyError as err:
            print ("git config not supplied :: Error: %s :: exiting", err)
            sys.exit(1)
        try:
            consul_config = cfg_data['consul_config']
            consul_cfg_data = self.read_yaml(config_file=consul_config)
            if consul_cfg_data:
                cfg_data.update(consul_cfg_data)
        except KeyError as err:
            print ("consul config not supplied :: Error: %s :: exiting", err)
            sys.exit(1)
        try:
            consul_data = {}
            cfg_data["consul_inject"] = {}
            for consul_key, consul_value in cfg_data['consul_data_configs'].items():
                consul_data["consul_data"] = self.read_yaml(config_file=consul_value)
                if consul_data["consul_data"]:
                    cfg_data["consul_inject"].update(consul_data["consul_data"])
        except KeyError as err:
            print ("consul data not Found :: Error: %s", err)
            sys.exit(1)

        return cfg_data

    def scan_yaml(self, raw_cfg=None):
        ## combine the various configs into 1 config
        raw_cfg = self.combine_config(cfg_data=raw_cfg)
        ## process the config
        if self.options.debug:
            debug = self.options.debug
            debug_name = ''
            if debug == 1:
                debug_name = 'critical'
            elif debug == 2:
                debug_name = 'error'
            elif debug == 3:
                debug_name = 'warning'
            elif debug == 4:
                debug_name = 'info'
            elif debug == 5:
                debug_name = 'debug'
            else:
                print ("Invalid debug level set, using default")
                debug_name = ''
            if debug_name:
                raw_cfg['logging_config']['log_level'] = debug_name

        user = os.getenv("SUDO_USER")
        actual_user = os.getenv("USER")
        if not self.options.force:
            if actual_user == 'root':
                print ("Error :: Please do not run me as: %s :: Exiting ", actual_user)
                sys.exit(1)
        if not user:
            if not actual_user:
                actual_user = "unknown"
            user = actual_user

        for key in raw_cfg:
            if key == 'git_config':
                for repo in raw_cfg[key]:
                    try:
                        if self.option.branch:
                            raw_cfg[key][repo]['branch'] = self.options.branch
                    except AttributeError:
                        pass
                    try:
                        raw_cfg[key][repo]['branch']
                    except KeyError:
                        # ''' still cant find a branch - force it to be master '''
                        raw_cfg[key][repo]['branch'] = 'master'

                    try:
                        clone_path = raw_cfg[key][repo]['clone_path']
                        if not re.search(user, clone_path):
                            gitclone_path, gitclone_dir = os.path.split(clone_path)
                            gitclone_path = os.path.join(gitclone_path, user)
                            clone_path = os.path.join(gitclone_path, gitclone_dir)
                            raw_cfg[key][repo]['clone_path'] = clone_path
                    except KeyError as err:
                        print ("Error :: %s", str(err))
                        sys.exit(1)

            if key == 'consul_config':
                try:
                    if self.options.token:
                        raw_cfg[key]['acl_token'] = self.options.token
                except AttributeError:
                    pass
                try:
                    if self.options.sslverify:
                        raw_cfg[key]["ssl_verify"] = self.options.sslverify
                except AttributeError:
                    pass
                try:
                    if self.options.host:
                        raw_cfg[key]['host'] = self.options.host
                except AttributeError:
                    pass
                try:
                    if self.options.port:
                        raw_cfg[key]['port'] = self.options.port
                except AttributeError:
                    pass

                try:
                    raw_cfg[key]['acl_token']
                except KeyError:
                    new_pass = getpass.getpass('Please Provide ACL Token')
                    if len(new_pass) == 0:
                        print ("Assuming no token Required :: Continuing")
                        raw_cfg[key]['acl_token'] = new_pass
                    else:
                        raw_cfg[key]['acl_token'] = new_pass
                try:
                    host = raw_cfg[key]['host']
                    port = raw_cfg[key]['port']
                    if raw_cfg[key]["use_ssl"]:
                        raw_cfg[key]['url'] = "https://" + host + ":" + port
                    else:
                        raw_cfg[key]['url'] = "http://" + host + ":" + port
                except (KeyError, AttributeError) as err:
                    print ("Consul Config Error :: %s", str(err))
                    sys.exit(1)

        '''add all of the command options to the config file for good measure'''
        raw_cfg['options'] = self.options
        return raw_cfg

