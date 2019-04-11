# coding:utf-8

import datetime
import hashlib
import math
import re
import time

import pytz

from localtime import tz, timenow

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

_RE_WEIBO = re.compile(ur'\d{1,2}')


def get_cp_as():
    i = int(math.floor(int(time.time())))
    t = hex(i).upper().replace('0X', '')
    m2 = hashlib.md5()
    m2.update(str(i))
    e = str(m2.hexdigest()).upper()
    if (8 != len(t)):
        asnew = "479BB4B7254C150"
        cp = "7E0AC8874BB0985"
    else:
        o = ""
        c = ""
        s = e[0:5]
        a = e[-5:]
        for n in range(0, 5):
            o += s[n] + t[n]
        for r in range(0, 5):
            c += t[r + 3] + a[r]
        asnew = "A1" + o + t[-3:]
        cp = t[0:3] + c + "E1"
    return asnew, cp


def weibodate(s):
    l = _RE_WEIBO.findall(s)
    lenght = len(l)
    now = timenow()
    if lenght == 1:
        date = now - datetime.timedelta(minutes=int(l[0]))
    elif lenght == 2:
        date = datetime.datetime(now.year, now.month, now.day, *map(int, l), tzinfo=tz)
    elif lenght == 4:
        date = datetime.datetime(now.year, *map(int, l), tzinfo=tz)
    elif lenght == 5:
        date = datetime.datetime(*map(int, l), tzinfo=tz)
    else:
        date = now
    return date.strftime("%a, %d %b %Y %H:%M:%S %z")


def zhihudate(date, hour):
    return datetime.datetime.strptime(date + hour[-2:], '%Y%m%d%H') \
        .replace(tzinfo=tz) \
        .strftime("%a, %d %b %Y %H:%M:%S %z")


def weixindate(timestamp):
    return datetime.datetime.utcfromtimestamp(int(timestamp)) \
        .replace(tzinfo=pytz.utc).astimezone(tz) \
        .strftime("%a, %d %b %Y %H:%M:%S %z")


def rsplit(s, count):
    f = lambda x: x > 0 and x or 0
    return [s[f(i - count):i] for i in range(len(s), 0, -count)]


def id2mid(id):
    result = ''
    for i in rsplit(id, 7):
        str62 = base62_encode(int(i))
        result = str62.zfill(4) + result
    return result.lstrip('0')


def base62_encode(num, alphabet=ALPHABET):
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)
