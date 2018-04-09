#
##
##########################################################################
#                                                                        #
#       consul-injector :: sorter                                        #
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

class DataSort(object):
    def __init__(self):
        self.sorted_data = {}

    def recursor(self, key='', value=None):
        if isinstance(value, dict):
            for nk, nv in value.items():
                fk = "{}/{}".format(key, nk)
                self.recursor(key=fk, value=nv)
        elif isinstance(value, list):
            for i, nv in enumerate(value):
                fk = "{}[{}]".format(key, i)
                self.recursor(key=fk, value=nv)
        else:
            self.sorted_data[key] = value
        return self.sorted_data
