import argparse


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='The true detector.')

    def prepare_args(self):
        self.parser.add_argument(
            'information',
            action='store',
            default='the Oxford Dictionaries Word of the Year 2016 is post-truth ',
            type=str,
            metavar='info',
            help='A sentence which should be tested')

        self.parser.add_argument(
            'option',
            action='store',
            choices=[
                'film',
                'actor',
                'none'],
            type=str,
            metavar='option',
            default='none',
            help='An additional option to test given sentence.')

    def get_parser(self):
        self.prepare_args()
        return self.parser.parse_args()
