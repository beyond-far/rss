#!/usr/bin/env python
# coding:utf8

import json

import tornado.gen
import tornado.httpclient
import tornado.web
from pyquery import PyQuery as pq
from utils.filters import get_cp_as


class Toutiao(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        uid = self.get_argument('uid', None)
        mid = self.get_argument('mid', None)
        if uid and mid:
            headers = {
                'Authority': 'www.toutiao.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3500.0 Safari/537.36',
            }
            asnew, cp = get_cp_as()
            url = 'http://www.toutiao.com/pgc/ma_mobile/?page_type=1&max_behot_time=0&aid=&media_id={}&count=10&version=2&as={}&cp={}&timestamp=1476282741654'.format(
                uid, asnew, cp)
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield client.fetch(url, headers=headers)
            if response.error:
                raise tornado.web.HTTPError(response.code)
            else:
                html = json.loads(response.body)['html']

                doc = pq(html)
                items = []
                for each in doc('section').items():
                    item = dict()
                    if each('img'):
                        preview = '<img referrerpolicy="no-referrer" src="https://picservice.qimai.cn/get/{}" />'.format(
                            each('img').attr['alt-src'])
                    else:
                        preview = ''
                    content = u"%s%s" % (each('h3').text(), preview)
                    item['content'] = content
                    item['title'] = each('h3').text()
                    item['link'] = "https://www.toutiao.com/item/{}/".format(each.attr['data-id'])
                    item['created'] = each('span.time').attr.title
                    item['guid'] = item['link']
                    item['author'] = each('.label-src').text()
                    items.append(item)

                pubdate = items[0]['created']
                link = "https://www.toutiao.com/c/user/{}/".format(mid)
                title = items[0]['author']
                self.set_header("Content-Type", "application/xml")
                self.render("rss.xml", title=title, description=title, items=items, pubdate=pubdate, link=link)
        else:
            self.redirect("/")
