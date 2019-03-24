from grab.spider import Spider, Task


class Parser(Spider):

    def __init__(self, page_titles):
        super().__init__()
        self.movie_names = page_titles
        self.initial_urls = ['https://ru.wikiquote.org/wiki/' + title for title in page_titles]
        self.quotes = {}

    def task_initial(self, grab, task):
        movie_name = ''
        for name in self.movie_names:
            if name in task.url:
                movie_name = name

        quotes = []
        for elem in grab.doc.select('//div[@class="poem"]/p'):
            quotes.append(elem.text())

        self.quotes[movie_name] = quotes
