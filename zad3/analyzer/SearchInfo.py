import urllib
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from google import search


class SearchInfo:

    def search_article(self, information):

        articles = []
        try:
            for url in search(
                    information,
                    lang='en',
                    num=1,
                    stop=5,
                    pause=2.0):
                articles.append(url)
        except urllib.error.HTTPError:
            return
        return articles

    def truth2_analyzer(self, given_sentence):

        false_links = []
        try:
            true_links = self.search_article(given_sentence)
            true_links += self.search_article(given_sentence + ' true') + self.search_article(
                given_sentence + ' fact') + self.search_article(given_sentence + ' news')

            false_links += self.search_article(given_sentence + ' false') + self.search_article(
                given_sentence + ' fake news') + self.search_article(given_sentence + ' myth')
        except TypeError:
            print("SEARCHINFO: Problem with google search")
            return

        score_true_ratio = 0
        true_counter = 0
        score_false_ratio = 0
        false_counter = 0

        for t in true_links:
            page = requests.get(t)
            soup = BeautifulSoup(page.content, 'html.parser')
            score_true_ratio += fuzz.partial_ratio(given_sentence, soup)
            true_counter += 1

        for t in false_links:
            page = requests.get(t)
            soup = BeautifulSoup(page.content, 'html.parser')
            score_false_ratio += fuzz.partial_ratio(given_sentence, soup)
            false_counter += 1

        score_true_ratio /= true_counter
        score_false_ratio /= false_counter

        if score_true_ratio > score_false_ratio:
            print(
                "SEARCHINFO: Sentence " +
                given_sentence +
                " is probably true.")
            return
        else:
            print(
                " SEARCHINFO: Sentence " +
                given_sentence +
                "is probably false.")
            return
