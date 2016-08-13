# coding:utf-8

from handlers import weibo, index

urls=[
    (r"/", index.MainHandler),
    (r"/weibo", weibo.WeiboHandler),
]
