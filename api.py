import asyncio
import logging

import requests

URL = 'http://192.168.43.177:8080/' #http://10.100.111.52:8080/'

class Api():

    def __init__(self):
        pass

    def get_questions(self, text):
        try:
            session = requests.Session()

            body = {
                'text': text
            }

            R = session.post(url=URL + 'generate', json=body)
            return R.json()
        except Exception as e:
            logging.exception(e)
            return []

    def analise(self, text):
        session = requests.Session()

        body = text.encode('utf-8')

        R = session.post(url=URL + 'analise', data=body)
        return R.json()

    async def questions_async(self, text):
        loop = asyncio.get_event_loop()
        body = {
            'text': text
        }
        future1 = loop.run_in_executor(None, requests.post, {'url':URL + 'generate', 'json':body})
        response1 = await future1
        return response1