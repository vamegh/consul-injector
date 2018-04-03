#
##
##########################################################################
#                                                                        #
#       consul-injector :: socket_lock                                   #
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

import sys, logging


def lock(name=''):
    '''create a unix socket, if it already exists the program exits
       (ensures only 1 instance is running at a time)'''
    socket_name = '\0' + name
    try:
        import socket
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(socket_name)
        return s
    except socket.error as err:
        logging.error("%s is already running :: error_message: %s", name, str(err))
        sys.exit(1)
