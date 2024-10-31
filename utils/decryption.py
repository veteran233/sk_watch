import requests
import re
import pickle

__all__ = ['getMainjs', 'getSeed']

b_patten = r'(?<!\')\{(?!\\x20)|(?<!\\x20)\}(?!\')'
MAX_P = int(5e5)


def _moveCur(s: str, i, p):
    while i:
        i -= 1
        s = s[re.search(p, s).end():]
    return s


def _getFuncPos(body: str, is_reverse=False):
    ret = []
    pos = 0

    while True:
        bracket_match = 0
        r = re.search(b_patten, body)
        if r is None: break

        body = body[r.end() - 1:]
        begin = pos + r.end() - 1

        pos = begin
        while True:
            r = re.search(b_patten, body)
            if r is None: break

            cur = r.group()
            _pos = r.end()

            if cur == '{': bracket_match += 1
            else: bracket_match -= 1

            body = body[_pos:]
            pos += _pos

            if bracket_match == 0: break

        if r is not None:
            ret.append((begin, pos))
        else:
            break

    if is_reverse:
        for x, y in ret:
            x = len(body) - x
            y = len(body) - y
    return ret


def getMainjs():
    body = requests.get(
        url='http://203.104.209.199/kcs2/js/main.js',
        headers={
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        },
        timeout=30)
    with open('./main.js', 'w', encoding='utf8') as f:
        f.write(body.text)


def getSeed():
    with open('./main.js', 'r', encoding='utf8') as f:
        body = f.read()

    rdlist = None
    nobj = None
    bak_body = body

    front_body = body[:MAX_P]
    tail_body = body[-MAX_P:]

    front_func_pos = _getFuncPos(front_body)
    tail_func_pos = _getFuncPos(tail_body[::-1], True)

    def _f(func_pos, body):
        nonlocal rdlist
        nonlocal nobj
        for l, r in func_pos:
            func = body[l:r]

            var_cnt = len(re.findall('var ', func))
            for_cnt = len(re.findall('for ', func))
            while_cnt = len(re.findall('while ', func))
            if_cnt = len(re.findall('if ', func))
            typeof_cnt = len(re.findall('typeof ', func))
            return_cnt = len(re.findall('return ', func))

            judge = (var_cnt, for_cnt, while_cnt, if_cnt, return_cnt)

            if judge == (1, 0, 0, 0, 2) and typeof_cnt == 0:
                func = _moveCur(func, 1, '\[')
                rdlist = func[:re.search('\]', func).end() - 1].split(',')
            elif judge == (1, 0, 0, 0, 0) and typeof_cnt > 2:
                func = _moveCur(func, 1, '\(')
                nobj = func[:re.search('\)', func).end() - 1]

    _f(front_func_pos, front_body)
    _f(tail_func_pos, tail_body)

    if rdlist is None or nobj is None:
        raise Exception('update SEED failed!!!')

    nobj = int(nobj, 16)
    offset = nobj - rdlist.index("'B2jQzwn0'")

    nseed = (rdlist.index("'ue9svf9bueLFu0vfra'") + offset +
             len(rdlist)) % len(rdlist)

    bak_body = _moveCur(bak_body, 1, '\(' + hex(nseed) + '\)\]=\[')
    res = bak_body[:re.search('\]', bak_body).end() - 1].split(',')

    for _i in range(len(res)):
        res[_i] = int(res[_i], 16)

    with open('./seed.pkl', 'wb') as f:
        pickle.dump(res, f)
