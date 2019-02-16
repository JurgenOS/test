# -*- coding: utf-8 -*-
import logging
import os
import test_loger


@test_loger.log_run
def run():
    log_tracer = test_loger._LogTracer()
    log_file = os.path.join(log_tracer.log_dir_path, 'log.log')
    logging.basicConfig(format='%(asctime)s %(levelname)s  %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        filename=log_file,
                        level=logging.DEBUG)

    test_loger.some_function(10, 100)
    test_loger.some_function_1(10)


if __name__ == '__main__':
    run()