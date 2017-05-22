# coding:utf-8

import tornado.web
import tornado.httpclient
import tornado.gen
import json
from pyquery import PyQuery as pq
from utils.filters import weibodate, id2mid
from configs import WEIBO_URL, WEIBO_LINK, NEW_WEIBO_URL, NEW_WEIBO_API


class WeiboHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        uid = self.get_argument('uid', None)
        if uid and uid.isdigit() and len(uid) == 10:
            self.uid = uid
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield client.fetch(NEW_WEIBO_API.format(uid=uid))

            if response.error:
                raise tornado.web.HTTPError(response.code)
            else:
                cards = json.loads(response.body)['cards']
                retitle = u'{author}的微博'.format(author=cards[0]['mblog']['user']['screen_name'])
                items = []
                for card in cards:
                    item = {}
                    content = card['mblog']['text']
                    if card['mblog'].get('retweeted_status', None):
                        content += "//"
                        content += card['mblog']['retweeted_status']['text']
                        if card['mblog']['retweeted_status'].get('pics', None):
                            retweeted_pics = ''
                            for each in card['mblog']['retweeted_status']['pics']:
                                retweeted_pics += "<img src=%s />" % each['large']['url']
                            content += retweeted_pics

                    if card['mblog'].get('pics', None):
                        pics = ''
                        for each in card['mblog']['pics']:
                            pics += "<img src=%s />" % each['large']['url']
                        content += pics
                    title = pq(card['mblog']['text']).text()
                    mid = id2mid(card['mblog']['id'])
                    link = "http://weibo.com/%s/%s" % (self.uid, mid)
                    created = weibodate(card['mblog']['created_at'])

                    item['content'] = content
                    item['title'] = title
                    item['link'] = link
                    item['created'] = created
                    item['guid'] = item['link']
                    item['author'] = card['mblog']['user']['screen_name']
                    items.append(item)
                pubdate = items[0]['created']
                link = NEW_WEIBO_URL.format(uid=uid)
                self.set_header("Content-Type", "application/xml")
                self.render("rss.xml", title=retitle, description=retitle, items=items, pubdate=pubdate, link=link)
        else:
            self.redirect("/")
