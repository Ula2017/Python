from analyzer.LieDetector import LieDetector
from analyzer.Analysis import Analysis
from analyzer.SearchInfo import SearchInfo


class JAnalyzer:
    def lie_detector():
        a = LieDetector()
        b = a.read_file()
        c = a.ask_simply_question(b)
        print(c)

    def film_analyzer(category, argument):
        a = Analysis()
        a.search(category, argument)

    def anything_analyzer(argument):
        u = SearchInfo()
        u.truth2_analyzer(argument)

    def main():

        a = Analysis()
        a.search('film', 'Toy Story')
        a.search('film', 'toy story 5')
        a.search('actor', 'Morgan Freeman')
        u = SearchInfo()
        u.truth2_analyzer('Morgan Freeman isn\'t a God')
