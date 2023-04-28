# -*- coding: utf-8 -*-
import requests
import time
import re
from requests.exceptions import RequestException
from encode.srun_md5 import get_md5
from encode.srun_sha1 import get_sha1
from encode.srun_base64 import get_base64
from encode.srun_xencode import get_xencode


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
}
init_url = "http://210.43.112.9"
get_challenge_api = "http://210.43.112.9/cgi-bin/get_challenge"
srun_portal_api = "http://210.43.112.9/cgi-bin/srun_portal"
n = '200'
tp = '1'
ac_id = '5'
enc = "srun_bx1"


def get_chksum():
    chkstr = token + username
    chkstr += token + hmd5
    chkstr += token + ac_id
    chkstr += token + ip
    chkstr += token + n
    chkstr += token + tp
    chkstr += token + i
    return chkstr


def get_info():
    info_temp = {
        "username": username,
        "password": password,
        "ip": ip,
        "acid": ac_id,
        "enc_ver": enc
    }
    i = re.sub("'", '"', str(info_temp))
    i = re.sub(" ", '', i)
    return i


def init_ip():
    global ip
    init_res = requests.get(init_url, headers=header)
    print("初始化获取ip...")
    ip = re.search('id="user_ip" value="(.*?)"', init_res.text).group(1)
    print("ip:" + ip)


def get_token():
    print("获取token...")
    global token
    get_challenge_params = {
        "callback": "jQuery1124069737681976102_" + str(int(time.time()*1000)),
        "username": username,
        "ip": ip,
        "_": int(time.time()*1000),
    }
    get_challenge_res = requests.get(
        get_challenge_api, params=get_challenge_params, headers=header)
    token = re.search('"challenge":"(.*?)"', get_challenge_res.text).group(1)
    # print(get_challenge_res.text)
    print("token:" + token)


def complex_token():
    global i, hmd5, chksum
    i = get_info()
    i = "{SRBX1}" + get_base64(get_xencode(i, token))
    hmd5 = get_md5(password, token)
    chksum = get_sha1(get_chksum())
    print("加密已完成")


def net_login():
    srun_portal_params = {
        'callback': 'jQuery1124069737681976102_' + str(int(time.time()*1000)),
        'action': 'login',
        'username': username,
        'password': '{MD5}' + hmd5,
        'ac_id': ac_id,
        'ip': ip,
        'chksum': chksum,
        'info': i,
        'n': n,
        'type': tp,
        'os': 'windows 10',
        'name': 'windows',
        'double_stack': '0',
        '_': int(time.time()*1000)
    }
    # print(srun_portal_params)
    srun_portal_res = requests.get(
        srun_portal_api, params=srun_portal_params, headers=header)
    # print(srun_portal_res.text)
    print("网络已连接")


if __name__ == '__main__':
    global username, password
    username = "" #填写账号 
    password = "" #填写密码
    try:
        print("网络连接已开始...")
        init_ip()
        get_token()
        complex_token()
        net_login()
    except RequestException:
        print("网络连接超时！")
