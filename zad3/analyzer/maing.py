from LieDetector import LieDetector
from Analysis import Analysis
from SearchInfo import SearchInfo
from ArgumentParser import ArgumentParser


def main():

    parser = ArgumentParser()
    args = parser.get_parser()
    sentence = args.information
    opt = args.option

    if opt.lower() == 'film' or opt.lower() == 'actor':
        analyser = Analysis()
        analyser.search(opt, sentence)
    s = SearchInfo()
    s.truth2_analyzer(sentence)

    l = LieDetector()
    l.do_search()


if __name__ == '__main__':
    main()
