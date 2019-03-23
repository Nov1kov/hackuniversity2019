
import argparse

from api import Api
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

    #print(api.analise('Крупнейший по численности населения город России и её субъект — 12 615 882[2] чел. (2019)'))
    infos = []
    results = wiki_api.quotes('Бойцовский')
    for result in results:
        summaries = wiki_api.quotes(result)
        for info in summaries:
            logging.info(info)
            infos.append(info)

    text_for_generate = '\n'.join(infos)
    questions = api.get_questions(text_for_generate)
    print(questions)
