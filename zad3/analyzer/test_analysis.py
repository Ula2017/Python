from analyzer.Analysis import Analysis

actor = Analysis()
r = actor.get_page_actor('Troian', 'Bellisario')
assert actor.get_html_prepared(r) == "Exists"
r = actor.get_page_actor('Troian', 'Belli')
assert actor.get_html_prepared(r) == "Not exists"
film = Analysis()
r = film.get_page_film("Toy Story")
assert film.get_html_prepared_film(r, "Toy Story") == "Exists"
r = film.get_page_film("toy Story")
assert film.get_html_prepared_film(r, "toy Story") == "Exists"
r = film.get_page_film("toy story 2")
assert film.get_html_prepared_film(r, "toy story 2") == "Exists"
r = film.get_page_film("toy story 5")
assert film.get_html_prepared_film(r, "toy story 5") == "Not exists"

assert actor.search("singer", "Michael Jackson") == -1
assert 0 == actor.search('actor', 'Troian Bellisario')
assert 0 == actor.search('film', 'Troian Bellisario')
assert 0 == actor.search('film', 'Toy Story')
assert 0 == actor.search('film', 'Toy Story 5')
