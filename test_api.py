
import argparse

from api import Api
from grabber import Parser
from wiki_api import WikiApi


import logging

# create logger
from wiki_api import WikiApi

logger = logging.getLogger('')
logger.setLevel(logging.NOTSET)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.NOTSET)
logger.addHandler(ch)
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-keys', type=str, nargs='+')

if __name__=="__main__":
    args = parser.parse_args()

    wiki_api = WikiApi()
    api = Api()

    links = []
    movies_by_category = []
    for page_title in wiki_api.quotes("Бойцовский Клуб"):
        page = wiki_api.quote_page(page_title)
        if page and page.categories:
            category = page.categories[0]
            movies_by_category = wiki_api.get_pages_by_categories(category)
        links.append('https://ru.wikiquote.org/wiki/' + page_title)

    parser = Parser(links)
    parser.run()
    for q in parser.quotes:
        print(q)
