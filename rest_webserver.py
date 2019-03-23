import logging

from aiohttp import web
import json

from api import Api
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
    result = {
        'questions' : questions,
        'pages': results,
        'original': text_for_generate
    }
    text = json.dumps(result, indent=2, ensure_ascii=False)
    logging.info(text)
    return web.Response(text=text)


app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/quiz', new_quiz)

web.run_app(app)
