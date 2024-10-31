import math
import random
import requests
import pickle
from datetime import datetime

PORT_API_SEED = []
token = 'ecd37b81c06bd22f990c0ba69729bf3cddfa91c6'


def rd(x):
    return math.floor(random.random() * x)


def generateRankKey(userid):
    t = userid
    e = PORT_API_SEED[t % 10]
    i = math.floor(datetime.now().timestamp())
    n = 1000 * (rd(9) + 1) + t % 1000
    o = rd(8999) + 1000
    r = rd(32767) + 32768
    s = rd(10)
    a = rd(10)
    _ = rd(10)
    u = int(str(t)[:4])
    l = (4132653 + r) * (u + 1000) - i + (1875979 + 9 * r)
    c = l - t
    h = c * e
    p = str(n) + str(h) + str(o)
    p = str(s) + p
    d = str(p)[:8]
    f = str(p)[8:]
    p = d + str(a) + f
    d = p[:18]
    f = p[18:]
    p = d + str(_) + f
    return p + str(r)


async def getRawData(page):
    if isinstance(page, int): page = str(page)

    global PORT_API_SEED
    with open('./seed.pkl', 'rb') as f:
        PORT_API_SEED = pickle.load(f)

    url = 'http://203.104.209.199/kcsapi/api_req_ranking/mxltvkpyuklh'
    userid = 8156938
    ranking = generateRankKey(userid)
    now = str(int(datetime.now().timestamp() * 1000))

    ret = requests.post(
        url,
        "api_pageno=" + page + "&api_verno=1&api_ranking=" + ranking +
        "&api_token=" + token,
        headers={
            'Content-Type':
            'application/x-www-form-urlencoded',
            'Referer':
            'http://203.104.209.199/kcs2/index.php?api_root=/kcsapi&voice_root=/kcs/sound&osapi_root=osapi.dmm.com&version=5.1.4.1&api_token='
            + token + '&api_starttime=' + now,
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }).text

    return eval(ret[7:])['api_data']['api_list']


def getUserData(uid):
    if isinstance(uid, int): uid = str(uid)

    url = 'http://203.104.209.199/kcsapi/api_req_member/get_practice_enemyinfo'
    nn = datetime.now()
    now = str(int(nn.timestamp() * 1000))

    ret = requests.post(
        url,
        'api_token=' + token + '&api_verno=1&api_member_id=' + uid,
        headers={
            'Content-Type':
            'application/x-www-form-urlencoded',
            'Referer':
            'http://203.104.209.199/kcs2/index.php?api_root=/kcsapi&voice_root=/kcs/sound&osapi_root=osapi.dmm.com&version=5.1.4.1&api_token='
            + token + '&api_starttime=' + now,
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        })
