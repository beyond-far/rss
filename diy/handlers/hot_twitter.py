#!/usr/bin/env python
# coding:utf8

import tornado.web
import tornado.httpclient
import tornado.gen
from pyquery import PyQuery as pq


class HotTwitter(tornado.web.RequestHandler):
	@tornado.gen.coroutine
	def get(self):
		url = 'https://frontbin.com/hot'
		client = tornado.httpclient.AsyncHTTPClient()
		response = yield client.fetch(url)
		if response.error:
			raise tornado.web.HTTPError(response.code)
		else:
			content = response.body
			pq_content = pq(content)
			title = pq_content('title').text()
			items = []
			for each in pq_content('.list__item').items():
				item = {}
				img_list = ['<img src="'+a('a').attr.href.replace('medium', 'large')+'">' for a in each('figure').items() if a('a').attr.href]
				if img_list:
					each('.list__item__pic-wrapper').remove()
					item['content'] = each('.list__item__content').html()+''.join(img_list)
				else:
					item['content'] = each('.list__item__content').html()
				item['created'] = each('.cf:eq(0) > span[class="muted fr"]').text()
				item['title'] = each('.list__item__content').text()
				item['link'] = each(u'a:contains("原文")').attr.href
				item['guid'] = item['link']
				item['author'] = each('.cf:eq(0) .name').text() + each('.cf:eq(0) .screen-name').text()
				items.append(item)

			pubdate = items[0]['created']
			link = url
			self.set_header("Content-Type", "application/xml")
			self.render("rss.xml", title=title, description=title, items=items, pubdate=pubdate, link=link)
