 # -*- coding: utf-8 -*-


from twisted.internet import reactor
from scrapy.crawler import Crawler,CrawlerRunner,CrawlerProcess
from scrapy.utils.project import get_project_settings




class RunSpider(object):
    def __init__(self):
        self.process = CrawlerProcess(get_project_settings())
        #self._get_setting()
        #self.runner = CrawlerRunner()
        #self.runner.signals.connect(add_item, signal=signals.item_passed)
        #self.runner.signals.connect(reactor.stop, signal=signals.spider_closed)

    def runOneSpider(self,Onespider):
        self.process.crawl(Onespider)
        self.process.start(stop_after_crawl=True)
        """
        :param spider:the spider is the name of spider,not spider class,
        :return:
        """
        #self.runner.crawl(Onespider)
       # d = self.runner.join()
        #d.addBoth(lambda _: reactor.stop())
        #reactor.run(installSignalHandlers=0 )

    def runMulSpider(self,*spider):
        for crawl in spider:
            self.process.crawl(crawl)
        self.process.start()


if __name__ == "__main__":
    spider = RunSpider()
    spider.runOneSpider('51job')
    print 'yes'




