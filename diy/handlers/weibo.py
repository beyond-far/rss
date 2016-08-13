# coding:utf-8

import tornado.web
import tornado.httpclient
import tornado.gen
import lxml.html
import re

from utils.filters import weibodate
from configs import WEIBO_URL, WEIBO_LINK


class WeiboHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        uid = self.get_argument('uid', None)
        print uid
        if uid and uid.isdigit() and len(uid) == 10:
            self.uid = uid
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield client.fetch(WEIBO_URL.format(uid=uid))

            if response.error:
                raise tornado.web.HTTPError(response.code)
            else:
                root = lxml.html.fromstring(response.body.decode('utf-8'))
                author = root.xpath('//*[@id="widget_wapper"]/div/div[1]/div[2]/div[1]/text()')[0]
                title = u'{author}的微博'.format(author=author)
                items = []
                for t in root.xpath('//*[@id="content_all"]/*/div[@class="wgtCell_con"]'):
                    item = {}
                    content = t.xpath('p[@class="wgtCell_txt"]')[0]
                    # convert thumbnail to bigpic
                    content_string = lxml.html.tostring(content, encoding='unicode')
                    content_string = re.sub('src="http://\w{3}.sinaimg.cn/thumbnail/','src="http://ww3.sinaimg.cn/mw690/', content_string)
                    
                    item['content'] = content_string
                    # print item['content']
                    item['title'] = content.text_content().split('\n')[0]
                    link = t.xpath('div/span[@class="wgtCell_tm"]/a')[0]
                    item['link'] = link.get('href')
                    item['created'] = weibodate(link.text)
                    item['guid'] = item['link']
                    item['author'] = author
                    items.append(item)
                pubdate = items[0]['created']
                link = WEIBO_URL.format(uid=uid)
                self.set_header("Content-Type", "application/xml")
                self.render("rss.xml", title=title, description=title, items=items, pubdate=pubdate, link=link)
        else:
            self.redirect("/")
