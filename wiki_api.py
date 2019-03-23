import logging
from urllib.parse import urlencode

import re
import requests
from mediawiki import MediaWiki
from mediawiki.utilities import memoize

WIKIPEDIA = "https://ru.wikipedia.org/w/api.php"

logger = logging.getLogger(__name__)


class WikiApi:

    def __init__(self):
        self.wikipedia = MediaWiki(lang='ru')
        self.wikiquote = CustomWikiEngine(url="https://{lang}.wikiquote.org/w/api.php",
                                   lang='ru')

    def quotes(self, *words):
        results = []

        for word in words:
            titles = self.wikiquote.quotes(word, results=4)
            results += titles

        return results

    def quote_page(self, title):
        response = {}
        try:
            response = self.wikiquote.page(title=title)
        except Exception as e:
            logging.exception(e)
        return response

    def movies(self):
        # https://ru.wikipedia.org/w/api.php?format=xml&action=query&list=embeddedin&einamespace=0&eilimit=500&eititle=Template:Infobox_film
        pass


    def search(self, *words):
        results = []

        for word in words:
            response = self.wikipedia.search(word, results=4)
            short_descriptions = response
            results += short_descriptions
        return results

    def opensearch(self, *words):
        results = []

        for word in words:
            response = self.wikipedia.opensearch(word)
            results += response
        return results

    def parse(self, *pages):
        results = []

        for page in pages:
            try:
                response = self.wikipedia.page(title=page)
                content = response.content
                sections = re.split(r'==.+?==', content)
                if sections:
                    summary = sections[0]
                    results.append(summary)
                    section_headers = re.findall(r'== \w+ ==', content)
                    if '== Сюжет ==' in section_headers:
                        index = section_headers.index('== Сюжет ==') + 1
                        if len(sections) > index:
                            plot = sections[index]
                            results.append(plot)
            except Exception as e:
                logging.error(e)
        return results


class CustomWikiEngine(MediaWiki):

    @memoize
    def quotes(self, query, results=10):
        """ Search for similar titles

            Args:
                query (str): Page title
                results (int): Number of pages to return
                suggestion (bool): Use suggestion
            Returns:
                tuple or list: tuple (list results, suggestion) if \
                               suggestion is **True**; list of results \
                               otherwise """

        self._check_query(query, "Query must be specified")

        search_params = {
            "list": "search",
            #"srprop": "",
            "srlimit": results,
            "srsearch": query,
        }

        raw_results = self.wiki_request(search_params)

        self._check_error_response(raw_results, query)

        search_results = [d["title"] for d in raw_results["query"]["search"]]
        return search_results
