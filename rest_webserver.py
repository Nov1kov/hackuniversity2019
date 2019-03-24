import logging
from random import randrange

from aiohttp import web
import json

from api import Api
from grabber import Parser
from wiki_api import WikiApi


logger = logging.getLogger('')
logger.setLevel(logging.NOTSET)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.NOTSET)
logger.addHandler(ch)


async def handle(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj))


def prepare(infos):
    result = '\n'.join(infos)
    import re
    replaced = re.sub(r'(\(.+?\))', '', result)
    return replaced


async def new_quiz(request):
    keys = request.query['key'].split(',')
    wiki_api = WikiApi()
    api = Api()

    # print(api.analise('Крупнейший по численности населения город России и её субъект — 12 615 882[2] чел. (2019)'))
    infos = []
    results = wiki_api.search(*keys)
    for result in results:
        summaries = wiki_api.parse(result)
        for info in summaries:
            logging.info(info)
            infos.append(info)

    text_for_generate = prepare(infos)
    questions = api.get_questions(text_for_generate)
    quote_question = quote_generator(wiki_api, keys[0])
    if quote_question and questions:
        questions.insert(0, quote_question)
    result = {
        'questions' : questions,
        'pages': results,
        'original': text_for_generate
    }
    text = json.dumps(result, indent=2, ensure_ascii=False)
    logging.info(text)
    return web.Response(text=text)


def quote_generator(wiki_api, search_word):
    page_titles = []
    movies_by_category = []
    for page_title in wiki_api.quotes(search_word):
        page = wiki_api.quote_page(page_title)
        if page and page.categories:
            category = page.categories[0]
            movies_by_category = wiki_api.get_pages_by_categories(category)
        page_titles.append(page_title)

    parser = Parser(page_titles)
    parser.run()
    if parser.quotes and len(movies_by_category) >= 3:
        quotes = []
        movie = ''
        while len(parser.quotes) > 0 and len(quotes) == 0:
            movie, quotes = parser.quotes.popitem()
        if not movie or not quotes:
            return {}
        wrong_answers = movies_by_category[:3]
        wrong_answers.insert(randrange(len(wrong_answers) + 1), movie)
        return  {
      "question": "Откуда эта цитата?\n" + quotes[0],
      "answers": wrong_answers,
      "rightAnswer": movie,
    }


app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/quiz', new_quiz)

web.run_app(app)
