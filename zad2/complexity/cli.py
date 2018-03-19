from argparse import ArgumentParser
from timeit import default_timer as timer
import numpy
import os
import sys
from math import log
import logging
import signal
import errno
from functools import wraps


parser = ArgumentParser(description='Program that estimates the complexity of given algorithm.')
parser.add_argument('initial_file', type=str, help=' file to initialize structure')
parser.add_argument('algorithm', type=str, help='file with algorithm')
parser.add_argument('clean_file', type=str, help='cleaning file')


class WrongArgError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def timeout(seconds, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


def print_message(complexity):
    option = {0: lambda: print('Complexity of algorithm is probably 1'),
              1: lambda: print('Complexity of algorithm is probably log(n)'),
              2: lambda: print('Complexity of algorithm is probably n'),
              3: lambda: print('Complexity of algorithm is probably nlog(n)'),
              4: lambda: print('Complexity of algorithm is probably n^2'),
              5: lambda: print('Complexity of algorithm is probably n^3')
              }

    option[complexity]()
    logging.info('Message about complexity was printed.')


def calculate_er(tab, compl, times, lambda_fun):

    result = []
    for e in range(len(compl)):
        value = (lambda_fun(compl[e]) * tab[0] - times[e])

        if len(tab) != 1:
            value = abs(tab[1]) + abs(value)

        result.append(value)

    result = numpy.average(result)
    return result


def match_complexity(results):
    type_complexity = [lambda n: 1, lambda n: log(n, 2), lambda n: n, lambda n: n * log(n, 2),
                       lambda n: n * n, lambda n: n * n * n]

    compl = []
    times = []
    offset = []

    for i in range(int(len(results)/2)):
        compl.append(results[2*i])
        times.append(results[2*i+1])

    temp_tab = numpy.polyfit([type_complexity[0](x) for x in compl], times, 0)
    x_tab = [type_complexity[0](x) for x in compl]
    dev = calculate_er(temp_tab, x_tab, times, type_complexity[0])
    offset.append(dev)

    temp_tab = numpy.polyfit([type_complexity[1](x) for x in compl], times, 1)
    x_tab = [type_complexity[1](x) for x in compl]
    dev = calculate_er(temp_tab, x_tab, times, type_complexity[1])
    offset.append(dev)

    temp_tab = numpy.polyfit([type_complexity[2](x) for x in compl], times, 1)
    x_tab = [type_complexity[2](x) for x in compl]
    dev = calculate_er(temp_tab, x_tab, times, type_complexity[2])
    offset.append(dev)

    temp_tab = numpy.polyfit([type_complexity[3](x) for x in compl], times, 1)
    x_tab = [type_complexity[3](x) for x in compl]
    dev = calculate_er(temp_tab, x_tab, times, type_complexity[3])
    offset.append(dev)

    temp_tab = numpy.polyfit([type_complexity[4](x) for x in compl], times, 1)
    x_tab = [type_complexity[4](x) for x in compl]
    dev = calculate_er(temp_tab, x_tab, times, type_complexity[4])
    offset.append(dev)

    temp_tab = numpy.polyfit([type_complexity[5](x) for x in compl], times, 1)
    x_tab = [type_complexity[5](x) for x in compl]
    dev = calculate_er(temp_tab, x_tab, times, type_complexity[5])
    offset.append(dev)

    print(offset)
    minim = abs(offset[0])
    num = 0
    i = 0
    for j in range(5):

        if abs(offset[i]) < minim:
            minim = abs(offset[i])
            print('jestem')
            num = i
        i += 1
    print('score', num)
    return print_message(num)


def time_predict(times, ns, fun, n):
    a = 0.0
    for i in range(len(times)):
        for j in range(len(times)):
            if i == j:
                continue
            a += abs(times[i] - times[j]) / (fun(ns[i]) - fun(ns[j]))
    a /= (len(times) - 1) ** 2

    b = 0.0
    for i in range(len(times)):
        b += times[i] - a * fun(ns[i])
    b /= range(len(times))

    return a * fun(n) + b


def open_file(file_name):
    try:
        init_file = open(file_name, 'r')
        return init_file
    except IOError:
        print('cannot open', file_name)
        sys.exit()


def prepare_args(file_name, prog_name):

    init_file = open_file(file_name)
    n = init_file.readline()
    n = n[:-1]
    try:
        n = int(n)
    except ValueError:
        raise WrongArgError('error')

    result = []

    for e in range(n):
        try:
            x = int(init_file.readline()[:-1])
        except ValueError:
            raise WrongArgError('error')
        result.append(x)
        args = init_file.readline()[:-1]
        try:
            result.append(measure_time(prog_name, args))
        except TimeoutError:
            print('Time is end.')
            sys.exit(1)

    print(result)
    return result


def build_string(file_name, args):
    command = 'python '
    command += file_name
    command += ' '
    command += args
    return command


@timeout(30, os.strerror(errno.ETIMEDOUT))
def measure_time(file_name, args):
    command = build_string(file_name, args)

    start = timer()
    os.system(command)
    stop = timer()

    return stop - start


def main():

    logging.basicConfig(filename='log_file.log', level=logging.DEBUG)
    logging.info('We just start our programme')
    argument = parser.parse_args()
    logging.info('Our arguments were parsed successfully.')
    try:
        result = prepare_args(argument.initial_file, argument.algorithm)
    except WrongArgError:
        print('Argument should be number.')
        sys.exit(1)

    match_complexity(result)

    clean_code = build_string(argument.clean_file, '')
    os.system(clean_code)

if __name__ == "__main__":
    main()
