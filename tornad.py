import json

import tornado.ioloop
import tornado.web

from rest_webserver import get_generated_quiz


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/quiz.html")


class GenerateQuizJson(tornado.web.RequestHandler):
    def get(self, data):
        keys = self.get_query_argument('key').split(',')
        result = get_generated_quiz(keys)
        text = json.dumps(result, indent=2, ensure_ascii=False)
        self.write(text)


class GenerateQuiz(tornado.web.RequestHandler):
    def get(self, data):
        keys = self.get_query_argument('key').split(',')
        result = get_generated_quiz(keys)
        questions = result['questions']
        for q in questions:
            if 'answers' not in q or not q['answers']:
                q['answers'] = []
        self.render("static/moderation.html", questions=questions)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/quiz(.*)", GenerateQuizJson),
        (r"/generate(.*)", GenerateQuiz),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
