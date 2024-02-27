import anti_useragent
import requests
import json
import random

header = {
    "User-Agent": anti_useragent.UserAgent().random
}
ip = []


def mainIP():
    # 获取IP
    ipurl = "https://ifconfig.me/ip"
    ipdata = requests.get(url=ipurl, headers=header).text
    ip.append(ipdata)
    return ipdata


def mainAdd():
    # ip归属地查询
    addra = f"https://whois.pconline.com.cn/ipJson.jsp?ip={ip[0]}&json=true"
    addra = requests.get(url=addra, headers=header).json()
    addrass = addra["pro"].replace("省", "") + ' ' + addra["city"].replace("市", "")
    return addrass
