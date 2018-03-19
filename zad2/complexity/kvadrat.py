from argparse import ArgumentParser
from math import log
import time
from random import randint

parser = ArgumentParser(description='Program that estimates the complexity of given algorithm.')
parser.add_argument('initial_file', type=int, help=' file to initialize structure')
parser.add_argument('dupa', type=str, help=' file to initialize structure')
def main():
	argument = parser.parse_args()
	c = argument.initial_file
	b=0
	alist = []
	for i in range(0, c):
            alist.append(randint(0, 100)) # need to import randint
	for i in range(argument.initial_file):
			sorted(alist)
	print('hello word')
	time.sleep(2)

if __name__ == "__main__":
    main()
