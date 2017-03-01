#-*- coding:utf-8 -*-

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from webspider.config.websetting import USER_AGENTS


class MyUserAgentDownloaderMiddleware(UserAgentMiddleware):

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self,value):
        self._user_agent = value

    def process_request(self, request, spider):
        self.user_agent = random.choice(USER_AGENTS)
        request.headers.setdefault('User-Agent', self.user_agent)


