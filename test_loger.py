# -*- coding: utf-8 -*-
#C:\Users\jos\WPy-3670\python-3.6.7.amd64\python.exe -i "$(FULL_CURRENT_PATH)"
import logging
import functools
import sys


class _LogTracer(object):
    def __init__(self):
        self._last_frame = None

    def tracer(self, frame, event, *extras):
        if event == 'return':
            self._last_frame = frame

    @property
    def last_frame(self):
        return self._last_frame

def log_locals_on_exit(fn):
    logging.basicConfig(level=logging.DEBUG)
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        log_tracer = _LogTracer()
        sys.setprofile(log_tracer.tracer)
        try:
            result = fn(*args, **kwargs)
        finally:
            sys.setprofile(None)
        frame = log_tracer.last_frame

        _locals = {}
        for k, v in frame.f_locals.items():
            _locals[k] = repr(v)
        logging.info(_locals)
        
        return result
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
    
    
some_function_1(3)

    