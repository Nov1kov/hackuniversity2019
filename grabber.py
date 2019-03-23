from grab.spider import Spider, Task


class Parser(Spider):

    def __init__(self, urls):
        super().__init__()
        self.initial_urls = urls
        self.quotes = []

    def task_initial(self, grab, task):

        for elem in grab.doc.select('//div[@class="poem"]/p'):
            self.quotes.append(elem.text())
