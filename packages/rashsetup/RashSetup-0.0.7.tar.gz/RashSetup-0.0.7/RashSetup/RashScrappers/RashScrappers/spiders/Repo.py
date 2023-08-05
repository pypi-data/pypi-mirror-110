import shutil

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import tempfile
import os


class TempHandler:
    def __init__(self, path=None):
        self.note = {
            False: [],
            True: []
        }

        self.temp = os.path.join(
            os.path.dirname(__file__) if not path else path if os.path.isdir(path) else os.path.dirname(path),
            "temp"
        )

        None if os.path.exists(self.temp) else os.mkdir(self.temp)

    def __call__(self, is_dir=False, suffix='', prefix='', dir_=None, text=True):

        if is_dir:
            path = tempfile.mkdtemp(suffix, prefix, dir_)
        else:
            mode, path = tempfile.mkstemp(suffix, prefix, dir_, text)
            os.close(mode)

        self.note[os.path.isdir(path)].append(path)
        return path

    def close(self):
        for _ in self.note[True]:
            shutil.rmtree(_)

        for _ in self.note[False]:
            os.remove(_)


class DirWalk:
    def __init__(self, root):
        self.handler = TempHandler()
        self.main_root = root
        self.root = self.handler(True, prefix="rash", dir_=self.handler.temp)

    def add_folder(self):
        pass  # adding a node

    def add_file(self):
        pass  # adding a left node

    def end_walk(self):
        pass


class RepoSpider(CrawlSpider):
    name = 'Repo'
    allowed_domains = ['github.com']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//div[@role='row']/div[@role='rowheader']/span/a",
            deny_extensions=set()  # allows any file
        ),
            callback='parse_item', follow=True
        ),
    )

    def __init__(
            self,
            url,
            pipe,
            save
    ):
        super().__init__()

        self.start_urls = url

        self.tree = DirWalk(save)
        self.pipe = pipe

    def start_requests(self):
        print("starting requests")
        yield scrapy.Request(self.start_urls)

    def parse_item(self, response):
        yield {
            "raw": response.urljoin(
                response.xpath("//div[@class='BtnGroup']/a[1]/@href").get()
            )
        }

        yield {
            "url": response.url
        }

    def parse_raw(self, response):
        self.logger.info("Parsing raw link for %s", response.url)

        yield {}
