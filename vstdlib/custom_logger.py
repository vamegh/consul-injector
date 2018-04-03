#
##
##########################################################################
#                                                                        #
#       consul-injector :: custom_logger                                 #
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

from datetime import datetime
import ctypes, logging, sys, os


def color_map(color='', c_map={}):
    '''This is the colour map -- used to generate the various different colours,
       this can be moved to config files later.'''
    color_map = {
        'black': '\033[0;30m',
        'blue': '\033[0;34m',
        'cyan': '\033[0;36m',
        'green': '\033[0;32m',
        'grey': '\033[0;37m',
        'red': '\033[0;4;31m',
        'wht_red': '\033[0;4;47;31m',
        'lgt_red': '\033[1;31m',
        'wht_lgt_red': '\033[1;4;47;31m',
        'yellow': '\033[1;33m',
        'blk_ylw': '\033[1;4;40;33m',
        'drk_grey': '\033[1;30m',
        'white': '\033[1;37m',
        'reset': '\033[0m',
        'debug': 'drk_grey',
        'info': 'blue',
        'warning': 'yellow',
        'error': 'lgt_red',
        'critical': 'red',
        'lvl_debug': 'grey',
        'lvl_info': 'green',
        'lvl_warning': 'blk_ylw',
        'lvl_error': 'wht_red',
        'lvl_critical': 'wht_lgt_red',
    }
    if c_map:
        try:
            # requested_color = c_map[color].encode('ascii')
            requested_color = c_map[color]
            try:
                requested_color = c_map[requested_color]
            except:
                ''' this aint a recursive lookup '''
            return requested_color
        except:
            ''' We dont really care, we just want to catch the exception, if it fails
                it defaults back to the built-in color map ...
                print ("requested colour not in custom colour map defaulting to built-in")'''
    requested_color = color_map[color]
    try:
        requested_color = color_map[requested_color]
    except:
        ''' this aint a recursive lookup '''
    return requested_color


class LevelFilter(logging.Filter):
    '''
      levels are not properly being propagated to log file - this is the solution
    '''

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno >= self.level


class CustomLog(logging.Formatter):
    '''This colours key elements from the logger, ie any element from the record'''

    def __init__(self, name='', config=None, *args, **kwargs):
        self.config = config
        self.name = name
        self.logger = ''
        try:
            self.color = config['color_map']
        except:
            self.color = ''
        try:
            self.logging_config = config['logging_config']
        except:
            self.logging_config = ''

        self._colors = {logging.DEBUG: color_map('debug', c_map=self.color),
                        logging.INFO: color_map('info', c_map=self.color),
                        logging.WARNING: color_map('warning', c_map=self.color),
                        logging.ERROR: color_map('error', c_map=self.color),
                        logging.CRITICAL: color_map('critical', c_map=self.color)}
        self._levels = {logging.DEBUG: color_map('lvl_debug', c_map=self.color),
                        logging.INFO: color_map('lvl_info', c_map=self.color),
                        logging.WARNING: color_map('lvl_warning', c_map=self.color),
                        logging.ERROR: color_map('lvl_error', c_map=self.color),
                        logging.CRITICAL: color_map('lvl_critical', c_map=self.color)}
        super(CustomLog, self).__init__(*args, **kwargs)

    def format(self, record):
        if self.config == 'disable_color':
            if self.name:
                record.levelname = self.name + " :: " + record.levelname
            return logging.Formatter.format(self, record)
        elif sys.stdout.isatty():
            record.msg = self._colors[record.levelno] + record.msg + color_map('reset')
            record.levelname = self._levels[record.levelno] + record.levelname + color_map('reset')
            return logging.Formatter.format(self, record)
        else:
            if self.name:
                record.levelname = self.name + " :: " + record.levelname
            return logging.Formatter.format(self, record)

    def exportLog(self, name=''):
        '''ColourLog method with no extra requirements - when we initialise the class we provide the config
           useful if we need to get access to the logger object, without having to pass configs through to this'''
        ## This makes the colourLog method completely redundant and that will be removed in due course.

        loglevel = 'INFO'
        self.logger = logging.getLogger()

        if not name:
            name = self.name
        if self.logging_config:
            try:
                loglevel = self.logging_config['log_level']
                loglevel = str.upper(self.loglevel)
            except:
                ''' loglevel defaults to INFO .. '''
            try:
                logfile = self.logging_config['log_file']
                log_path, log_file = os.path.split(logfile)
                log_file = name + '-' + log_file
                logfile = os.path.join(log_path, log_file)
                if not os.path.exists(log_path):
                    os.makedirs(log_path)
                try:
                    file_handler = logging.FileHandler(logfile)
                    file_handler.setLevel(loglevel)
                    file_style = CustomLog(name,
                                           'disable_color',
                                           '%(pathname)s - %(funcName)s - line:%(lineno)d :: %(asctime)s :: %(levelname)s :: %(message)s')
                    file_handler.setFormatter(file_style)
                    self.logger.addHandler(file_handler)
                except:
                    ''' we dont really care, -- just skip the logging file method entirely'''
                    print ("Unexpected error:", sys.exc_info()[0])
                    print ("skipping log file ...")
            except:
                ''' probably log_file key doesnt exist ... '''
                ''' its fine we ignore this if log_file isnt defined. '''
                print ("Unexpected error:", sys.exc_info()[0])
                print ("skipping log file ...")

        self.logger.setLevel(loglevel)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(loglevel)
        stream_style = CustomLog(name, config, '%(asctime)s - %(module)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_style)
        self.logger.addHandler(stream_handler)
        return self.logger

    def colourLog(self, name='', config=None):
        '''ColourLog method -- not the best way to do things, but allows us to pass through a name object'''
        ''' this is exactly the same as colourLog function below -- except its a class method - both methods work '''

        custom_color_map = config['color_map']
        logging_config = config['logging_config']
        self.logger = logging.getLogger()

        if logging_config:
            try:
                loglevel = logging_config['log_level']
                loglevel = str.upper(self.loglevel)
            except:
                ''' loglevel defaults to INFO .. '''
                loglevel = 'INFO'
            try:
                logfile_level = logging_config['log_file_level']
                logfile_level = str.upper(logfile_level)
            except:
                ''' logfile_level defaults to DEBUG .. '''
                logfile_level = 'DEBUG'
            try:
                logfile = logging_config['log_file']
                log_path, log_file = os.path.split(logfile)
                time_stamp = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
                log_file = name + '_' + time_stamp + '_' + log_file
                logfile = os.path.join(log_path, log_file)
                if not os.path.exists(log_path):
                    os.makedirs(log_path)
                try:
                    file_handler = logging.FileHandler(logfile)
                    file_style = CustomLog(name,
                                           'disable_color',
                                           '%(pathname)s - %(funcName)s - line:%(lineno)d :: %(asctime)s :: %(levelname)s :: %(message)s')
                    file_handler.setFormatter(file_style)
                    # file_handler.addFilter(LevelFilter(logfile_level))
                    file_handler.setLevel(logfile_level)
                    self.logger.addHandler(file_handler)
                except:
                    ''' we dont really care, -- just skip the logging file method entirely'''
                    print ("Unexpected error:", sys.exc_info()[0])
                    print ("skipping log file ...")
            except:
                ''' probably log_file key doesnt exist ... '''
                ''' its fine we ignore this if log_file isnt defined. '''
                print ("Unexpected error:", sys.exc_info()[0])
                print ("skipping log file ...")

        self.logger.setLevel(loglevel)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(loglevel)
        stream_style = CustomLog(name, config, '%(asctime)s - %(module)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_style)
        self.logger.addHandler(stream_handler)
        return self.logger

    def __del__(self):
        '''print "CustomLog Closed ..."'''


class StreamLog(logging.StreamHandler):
    '''This colours whole lines (works on the data stream)'''
    ''' and is seriously out of date -- not used so not updated for now. '''

    def __init__(self, c_map={}, *args, **kwargs):
        if c_map:
            self.color = c_map
        else:
            self.color = ''

        self._colors = {logging.DEBUG: color_map('debug', c_map=self.color),
                        logging.INFO: color_map('info', c_map=self.color),
                        logging.WARNING: color_map('warning', c_map=self.color),
                        logging.ERROR: color_map('error', c_map=self.color),
                        logging.CRITICAL: color_map('critical', c_map=self.color)}
        super(StreamLog, self).__init__(*args, **kwargs)

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def emit(self, record):
        try:
            message = self.format(record)
            stream = self.stream
            if not self.is_tty:
                stream.write(message)
            else:
                message = self._colors[record.levelno] + message + color_map('reset')
                stream.write(message)
            stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def customise(self, log_level, color_code):
        self._colors[log_level] = color_code

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            message = self._colors[record.levelno] + message + color_map('reset')
        return message

    def colourStream(self, loglevel='', logfile=''):
        '''Call this to initiate StreamLog'''
        self.loglevel = 'DEBUG'
        if loglevel:
            self.loglevel = str.upper(loglevel)
        if logfile:
            self.logfile = logfile
            log_path, log_file = os.path.split(logfile)
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            try:
                logging.basicConfig(filename=self.logfile,
                                    format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
            except IOError as e:
                print ("Log File issue: %s :: Error Code: %d :: Error: %s\n" % (self.logfile, e[0], e[1]))
                print ("skipping log file ...")
            except:
                print ("Unexpected error:", sys.exc_info()[0])
                print ("skipping log file ...")
        self.write = logging.getLogger()
        self.write.setLevel(self.loglevel)
        self.stream_handler = StreamLog()
        self.format_style = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.stream_handler.setFormatter(self.format_style)
        self.write.addHandler(self.stream_handler)
        return self.write

    def __del__(self):
        '''print "StreamLog Closed.."'''


def colourLog(name='', config=None):
    '''Call this to initiate CustomLog'''
    custom_color_map = config['color_map']
    logging_config = config['logging_config']
    ## pushing directly to root logger, ideally we would want to log
    ## per function / class call but that is just too much code to modify for now
    logger = logging.getLogger()
    if logging_config:
        try:
            loglevel = logging_config['log_level']
            loglevel = str.upper(loglevel)
        except:
            ''' loglevel defaults to INFO .. '''
            loglevel = 'INFO'
        try:
            logfile_level = logging_config['log_file_level']
            logfile_level = str.upper(logfile_level)
        except:
            ''' logfile_level defaults to DEBUG .. '''
            logfile_level = 'DEBUG'
        try:
            logfile = logging_config['log_file']
            log_path, log_file = os.path.split(logfile)
            time_stamp = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
            log_file = name + '_' + time_stamp + '_' + log_file
            logfile = os.path.join(log_path, log_file)
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            try:
                file_handler = logging.FileHandler(logfile)
                file_style = CustomLog(name,
                                       'disable_color',
                                       '%(pathname)s - %(funcName)s - line:%(lineno)d :: %(asctime)s :: %(levelname)s :: %(message)s')
                file_handler.setFormatter(file_style)
                # file_handler.addFilter(LevelFilter(logfile_level))
                file_handler.setLevel(logfile_level)
                logger.addHandler(file_handler)
            except:
                ''' we dont really care, -- just skip the logging file method entirely'''
                print ("Unexpected error:", sys.exc_info()[0])
                print ("skipping log file ...")
        except:
            ''' could match exact exceptions, but probably log_file key is missing '''
            ''' its fine we ignore this if log_file isnt defined. '''
            print ("Unexpected error:", sys.exc_info()[0])
            print ("skipping log file ...")

    logger.setLevel(loglevel)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(loglevel)
    stream_style = CustomLog(name, config, '%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(stream_style)
    logger.addHandler(stream_handler)
    ## this logger object can on other tools or even later in this tool be used to log each individual
    ## function or class logging call, for now the root logger is used -- it works and its pretty clean.
    return logger


def colourStream(loglevel='', logfile=''):
    '''Call this to initiate StreamLog'''
    if not loglevel:
        loglevel = 'DEBUG'
    if logfile:
        log_path, log_file = os.path.split(logfile)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        try:
            logging.basicConfig(filename=logfile,
                                format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
        except IOError as e:
            print ("Log File issue: %s :: Error Code: %d :: Error: %s\n" % (logfile, e[0], e[1]))
            print ("skipping log file ...")
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            print ("skipping log file ...")
    write = logging.getLogger()
    write.setLevel(loglevel)
    stream_handler = StreamLog()
    format_style = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(format_style)
    write.addHandler(stream_handler)
    return write

