#!/usr/bin/env python
# coding:utf8

import tornado.web
import tornado.gen
import tornado.httpclient
import json


class FanfouDigest(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        url = 'http://blog.fanfou.com/digest/json/index.json'
	client = tornado.httpclient.AsyncHTTPClient()
	response = yield client.fetch(url)
	if response.error:
            raise tornado.web.HTTPError(response.code)
	else:
	    daily_json = json.loads(response.body)[0]
	    daily_json_url = 'http://blog.fanfou.com/digest{0}'.format(daily_json.lstrip('.'))
            daily_response = yield client.fetch(daily_json_url)
	    if daily_response.error:
	        raise tornado.web.HTTPError(daily_response.code)
	    else:
		result = json.loads(daily_response.body)['msgs']
		items = []
		for each in result:
        	    item = {}
		    if each.get('img').get('preview', ''):
		        preview = '<img src="{0}">'.format(each.get('img').get('preview'))
		    else:
			preview = ''
		    content = u"%s%s" % (each.get('msg', ''), preview)
		    item['content'] = content
		    item['title'] = each.get('realname', '')
		    item['link'] = "http://fanfou.com/statuses/{0}".format(each.get('statusid', ''))
		    item['created'] = each.get('time', '')
		    item['guid'] = item['link']
		    item['author'] = each.get('loginname', '')
		    items.append(item)
		pubdate = items[0]['created']
		link = "http://blog.fanfou.com/digest/#/{0}".format(daily_json.replace('./json/', '').replace('.json', ''))
		title = u'饭否精选'
		self.set_header("Content-Type", "application/xml")
		self.render("rss.xml", title=title, description=title, items=items, pubdate=pubdate, link=link)


