from utils.data import getRawData
from utils.decryption import getMainjs, getSeed
from datetime import datetime
import pickle
import asyncio


async def _f():
    ret = []
    for _i in range(1, 101):
        ret.append(getRawData(_i))
    ret = await asyncio.gather(*ret)
    return ret


if __name__ == '__main__':

    try:
        ret = asyncio.run(_f())
    except Exception as e:
        getMainjs()
        getSeed()
        ret = asyncio.run(_f())

    dt = datetime.now()
    with open(
            f'./data/{dt.year:04d}{dt.month:02d}{dt.day:02d}_{dt.hour:02d}.pkl',
            'wb') as f:
        pickle.dump(ret, f)
