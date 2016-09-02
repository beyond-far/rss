# coding:utf-8

from handlers import weibo, index, fanfou_digest

urls=[
    (r"/", index.MainHandler),
    (r"/weibo", weibo.WeiboHandler),
    (r"/fanfou", fanfou_digest.FanfouDigest),
]
