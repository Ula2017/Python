from bs4 import BeautifulSoup
import requests
from analyzer.Exception import RequestError


class Analysis:

    def get_page_actor(self, person_name, person_surname):
        url = 'http://www.filmweb.pl/search?q='
        url += person_name.title() + '+' + person_surname.title()
        r = requests.get(url)
        if r.status_code != 200:
            raise RequestError
        return r

    def get_page_film(self, title):
        film = title.split(' ')
        url = 'http://www.filmweb.pl/search?q='
        for x in film:
            url += x + '+'
        r = requests.get(url)
        if r.status_code != 200:
            raise RequestError
        return r

    def get_html_prepared(self, r):
        soup = BeautifulSoup(r.content, 'html.parser')
        result = soup.find_all('div', class_='searchNoResults')
        if not result:
            return "Exists"
        return "Not exists"

    def get_html_prepared_film(self, r, film):
        soup = BeautifulSoup(r.content, 'html.parser')
        result = soup.find_all('a', class_="fImg125")
        if not result:
            return "Not exists"
        l = []
        for i in result:
            i = str(i)
            title = i.split("title=\" ", 1)[1].partition(' \"')
            l.append(title[0].lower())

        film = film.lower()
        for x in l:

            if x == film:

                return "Exists"

        return "Not exists"

    def search(self, kind, to_find):

        if kind == 'actor':
            inpt = to_find.split(' ')
            r = self.get_page_actor(inpt[0], inpt[1])
            result = self.get_html_prepared(r)
        elif kind == 'film':
            r = self.get_page_film(to_find)
            result = self.get_html_prepared_film(r, to_find)
        else:
            print("There is no category like " + kind)
            return -1

        if result == "Exists":
            if kind == 'actor':
                print("ANALYZER: Actor/Actress named " + to_find +
                      "  probably exists according to filmweb")
                return 0
            else:
                print("ANALYZER: Film " + to_find + " probably exists according to filmweb")
                return 0
        else:
            if kind == 'actor':
                print(
                    "ANALYZER: Actor/Actress named " +
                    to_find +
                    "  probably doesn't exist according to filmweb")
                return 0
            else:
                print(
                    "ANALYZER: Film " +
                    to_find +
                    "  probably doesn't exist according to filmweb")
                return 0
