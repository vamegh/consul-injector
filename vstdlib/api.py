#
##
##########################################################################
#                                                                        #
#       consul-injector :: api connector for consul                      #
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

import json
import requests
import sys
import os
import base64
import logging
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


class REST(object):
    def __init__(self, config=''):
        try:
            self.token = config["acl_token"]
        except KeyError as e:
            logging.error('''Configurations should be passed as a dict,
                containing url, acl_token, host and port key/values''')
            sys.exit(1)
        try:
            self.host = config["host"]
        except KeyError as e:
            logging.error('''Configurations should be passed as a dict,
                containing url, acl_token, host and port key/values''')
            sys.exit(1)
        try:
            self.port = config["port"]
        except KeyError as e:
            logging.error('''Configurations should be passed as a dict,
                containing url, acl_token, host and port key/values''')
            sys.exit(1)
        try:
            self.verify = config["verify_ssl"]
        except KeyError as e:
            self.verify = False

        try:
            url = config["url"]
        except KeyError as e:
            logging.error('''Configurations should be passed as a dict,
                containing url, login_pass, login_user, host and port key/values''')
            sys.exit(1)

        self.consul_url = url + '/v1/kv'
        self.consul_headers = {'X-Consul-Token': self.token}
        self.query_headers = {'Content-type': 'application/json', 'accept': 'application/json'}
        self.post_headers = {'Content-type': 'application/json', 'accept': 'application/json'}
        self.session = ''
        self.good_status = [200, 201, 202, 203, 204, 205, 206]

    def get(self, query=None):
        if query is None:
            return False
        if isinstance(query, dict):
            endpoint = list(query.keys())[0]
        else:
            endpoint = query
        query_url = self.consul_url + endpoint
        try:
            data = requests.get(query_url,
                                verify=self.verify,
                                headers=self.consul_headers)
        except Exception as e:
            logging.error("GET :: error :: ", str(e))
            return False
        except:
            logging.error("GET :: error :: ", sys.exc_info()[0])
            raise
        status_code = data.status_code
        if status_code in self.good_status:
            if data.json():
                full_data = data.json()
                for i, nv in enumerate(full_data):
                    json_data = base64.b64decode(nv["Value"])
                    full_data[i]["Value"] = json_data
                return full_data
        elif status_code == 401:
            logging.critical("Auth Error could not login using auth provided :: status: %s",
                             status_code)
            return False
        elif status_code == 500:
            logging.critical("Internal Server Error :: status: %s :: url: %s", status_code, query_url)
            return False
        else:
            logging.critical("Error :: status :: %s", status_code)
            if data.json():
                logging.error("Error :: %s", data.json())
            return False

    def put(self, payload=None):
        if payload is None:
            return False
        if isinstance(payload, dict):
            endpoint = list(payload.keys())[0]
            value = payload[endpoint]
            print ("Endpoint : {} :: Value: {}".format(endpoint, value))
        else:
            logging.error("Error: Payload must be JSON")
            sys.exit(1)
        post_url = self.consul_url +  endpoint
        try:
            data = requests.put(post_url,
                                 headers=self.consul_headers,
                                 verify=self.verify,
                                 data=value)
        except Exception as e:
            logging.error("error :: ", str(e))
            return False
        except:
            logging.error("error :: ", sys.exc_info()[0])
            raise
        status_code = data.status_code
        if status_code in self.good_status:
            return status_code
        elif status_code == 401:
            logging.critical("Auth Error could not login using auth provided :: status: %s",
                             status_code)
            return False
        elif status_code == 500:
            logging.critical("Internal Server Error :: status: %s :: url: %s", status_code, post_url)
            return False
        else:
            logging.critical("Error :: status :: %s", status_code)
            if data.json():
                logging.error("Error :: %s", data.json())
            return False
