import argparse


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Generating narcotic sounds.')

    def prepare_args(self):
        self.parser.add_argument(
            'file_name',
            action='store',
            default='midi_sound',
            type=str,
            metavar='file_name',
            help='the name of file with generate music')

        self.parser.add_argument(
            'loc',
            action='store',
            type=str,
            metavar='localisation',
            default='./',
            help='chosen localisation of generated music file')
        self.parser.add_argument(
            'tempo',
            default=120,
            type=int,
            choices=range(1, 200),
            metavar='tempo',
            help='set a tempo (1-200)')
        self.parser.add_argument(
            'octave_range',
            default=5,
            type=int,
            choices=range(0, 8),
            metavar='octave_range',
            help='set octave_range (1-8)')
        self.parser.add_argument(
            'opt',
            default=0,
            type=int,
            choices=range(0, 6),
            metavar='option',
            help='choose option (0-5)')

    def get_parser(self):
        self.prepare_args()
        return self.parser.parse_args()