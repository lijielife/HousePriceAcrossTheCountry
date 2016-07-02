# -*- coding: utf-8 -*-
import requests

city_reference = {'Bei Jing': u'北京', 'Shang Hai': u'上海', 'Guang Zhou': u'广州', 'Shen Zhen': u'深圳', 'Tian Jin': u'',
                  'Hang Zhou': u'杭州', 'Nan Jing': u'南京', 'Ji Nan': u'济南', 'Chong Qing': u'重庆', 'Qing Dao': u'青岛',
                  'Da Lian': u'大连', 'Ning Bo': u'宁波', 'Xia Men': u'厦门', 'Wu Han': u'武汉'}


class QFangWang(object):

    def __init__(self, city, website):
        print u'正在初始化爬虫...'
        self.city = city
        self.website = website
        self.root_url = 'http://' + self.city.lower().replace(" ", "") + self.website
        self.status_code = requests.get(self.root_url).status_code
        self.spider_pipeline = []
        self.add_to_pipeline(self.root_url)

    def __new__(cls, *args, **kwargs):
        print u'正在创建新的爬虫...'
        return object.__new__(cls, *args, **kwargs)

    def __del__(self):
        print u'{0}的房价抓取完毕!'.format(city_reference[self.city])

    @property
    def get_current_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def add_to_pipeline(self, link):
        self.spider_pipeline.append(link)

    def pop_from_pipeline(self):
        return self.spider_pipeline.pop()

    def pipeline_length(self):
        return len(self.spider_pipeline)

    def pipeline_is_empty(self):
        return len(self.spider_pipeline) is 0

    def worker(self):
        print u'正在抓取{0}的房价...'.format(city_reference[self.city])
        current_link = self.pop_from_pipeline()
        # heads = {
        #     'Host': "huaban.com",
        #     'Referer': "{http://huaban.com/boards/28195582/",
        #     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
        #     'X-Request': "JSON",
        #     'X-Requested-With': "XMLHttpRequest"
        # }
        # response = requests.get(current_link)

    def run(self):
        print self.get_current_time
        print u'正在连接{0}子网址，响应状态码为{1}'.format(city_reference[self.city], self.status_code)
        if self.status_code == 200:
            self.worker()
        else:
            print u'{0}子网址连接错误'.format(city_reference[self.city])