# 这里主要处理
import requests
import json
import re
import os
import time
import anti_useragent

proxies = {
    "http": "223.82.60.202:8060"
}

headers = {
    'cookie': 'kg_mid=625b3940e71fd7edbbcab0ff1a344294; kg_dfid=3w4YNS0105iM4QRTmB3A1Wgn; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1655613156; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1655617461',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': anti_useragent.UserAgent().random
}
music_datas = None
music_IDs = None
music_names = None


def mainKUGOU(key):
    global music_datas
    global music_IDs
    global music_names
    import time
    from hashlib import md5
    # 酷狗音乐加密算法
    time = int(time.time()) * 1000
    sign = ["NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt", "bitrate=0", "callback=callback123", "clienttime={}".format(time),
            "clientver=2000", "dfid=-", "inputtype=0", "iscorrection=1", "isfuzzy=0", "keyword={}".format(key),
            "mid={}".format(time), "page=1", "pagesize=30", "platform=WebFilter", "privilege_filter=0", "srcappid=2919",
            "token=", "userid=0", "uuid={}".format(time), "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"]
    sign = ''.join(sign)
    md5 = md5()
    md5.update(sign.encode('UTF-8'))
    jm = md5.hexdigest()
    url = f'https://complexsearch.kugou.com/v2/search/song?callback=callback123&keyword={key}&page=1&pagesize=30&bitrate=0&isfuzzy=0&inputtype=0&platform=WebFilter&userid=0&clientver=2000&iscorrection=1&privilege_filter=0&token=&srcappid=2919&clienttime={time}&mid={time}&uuid={time}&dfid=-&signature={jm}'

    # 请求网页获取音乐数据
    res = requests.get(url=url, headers=headers, proxies=proxies).text
    musicdata = res.replace('callback123(', '').replace(')', "").replace('(', '')
    musicdata = json.loads(musicdata)
    # 提取对应的音乐数据
    music = musicdata['data']['lists']
    music_names = []
    music_IDs = []  # 音乐专辑ID
    music_datas = []  # 音乐的hash
    for musiclist in music:
        music_name = musiclist['FileName']  # 音乐名称
        music_ID = musiclist['AlbumID']  # 音乐播放专辑ID
        music_data = musiclist['FileHash']  # 普通音乐hash值
        music_names.append(music_name)
        music_IDs.append(music_ID)
        music_datas.append(music_data)
    return music_names


def getmusic(ekey):
    # 将所有爬取到的数据名字写入程序展示
    # 拿到的数据有音乐名字、音乐歌手、音乐ID、音乐hash算法
    kgurl = f'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={music_datas[ekey]}&album_id={music_IDs[ekey]}'
    res = requests.get(url=kgurl, headers=headers, proxies=proxies).json()
    # 获取音乐的下载地址
    downurl = res['data']['play_url']
    req = requests.get(url=downurl, headers=headers, proxies=proxies).content
    with open("xwdownload/" + music_names[ekey] + '.mp3', mode="wb") as f:
        f.write(req)
        f.close()
    return music_names[ekey]
