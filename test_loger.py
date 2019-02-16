# -*- coding: utf-8 -*-
#C:\Users\jos\WPy-3670\python-3.6.7.amd64\python.exe -i "$(FULL_CURRENT_PATH)"
import logging
import functools
import sys
import os


class _LogTracer(object):
    def __init__(self):
        self._last_frame = None

    def tracer(self, frame, event, *extras):
        if event == 'call':
            self._last_frame = frame

    @property
    def last_frame(self):
        return self._last_frame

    @property
    def log_dir_path(self):
        if not os.path.exists('log'):
            os.mkdir('log')
        return os.path._getfullpathname('log')


log_tracer = _LogTracer()
log_file = os.path.join(log_tracer.log_dir_path, 'log.log')
logging.basicConfig(format='%(asctime)s %(levelname)s  %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=log_file,
                    level=logging.DEBUG)


def log_locals_on_exit(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):

        sys.setprofile(log_tracer.tracer)

        try:
            result = fn(*args, **kwargs)
        finally:
            sys.setprofile(None)

        frame = log_tracer.last_frame

        _locals = {}
        for k, v in frame.f_locals.items():
            _locals[k] = repr(v)

        if fn.__name__ == 'run':
            logging.info(fn.__name__)
            return result

        logging.debug(fn.__name__, _locals)
        
        return result
    return inner


def log_run(fn):
    logging.info(fn.__name__)

    @functools.wraps(fn)
    def inner(*args, **kwargs):
        return fn(*args, **kwargs)
    return inner


@log_locals_on_exit
def some_function(x, y):
    temp_1 = x+y
    temp_2 = x*y
    string = '{} {}'.format(temp_1,temp_2)
    print(string)
    return string  


@log_locals_on_exit
def some_function_1(x):
    temp = type(x)
    return x
    
    
some_function(3,5)
