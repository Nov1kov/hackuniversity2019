from grab.spider import Spider, Task


class Parser(Spider):

    def __init__(self, urls):
        super().__init__()
        self.urls = urls
        self.initial_urls = [urls[0]]

    def prepare(self):
        pass

    def task_initial(self, grab, task):

        for url in self.urls:
            yield Task('quote', url=url)

    def task_quote(self, grab, task):
        pass