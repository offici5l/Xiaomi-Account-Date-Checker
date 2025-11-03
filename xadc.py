#!/usr/bin/python

import requests
import json
import hashlib
from urllib.parse import parse_qs, urlparse
from datetime import datetime

User = "okhttp/4.12.0"
headers = {"User-Agent": User}
base_url = "https://account.xiaomi.com"

def parse(res): return json.loads(res.text[11:])

def login():
    
    sid = "passport"

    user = input('\nEnter user: ')
    pwd = input('\nEnter password: ')
    hash_pwd = hashlib.md5(pwd.encode()).hexdigest().upper()

    cookies = {}

    r = requests.get(f"{base_url}/pass/serviceLogin", params={'sid': sid, '_json': True}, headers=headers, cookies=cookies)

    cookies.update(r.cookies.get_dict())

    deviceId = cookies["deviceId"]

    data = {k: v[0] for k, v in parse_qs(urlparse(parse(r)['location']).query).items()}

    data.update({'user': user, 'hash': hash_pwd})

    r = requests.post(f"{base_url}/pass/serviceLoginAuth2", data=data, headers=headers, cookies=cookies)

    cookies.update(r.cookies.get_dict())

    res = parse(r)
    
    logindata = {"userId": res['userId'], "passToken": res['passToken'], "deviceId": deviceId}

    return logindata


logindata = login()
    
passToken = logindata["passToken"]

deviceId = logindata["deviceId"]

userId = logindata["userId"]

headers = {
  'User-Agent': User,
  'Accept-Encoding': "gzip",
  'Content-Type': "application/json",
  'content-type': "application/json; charset=utf-8",
  'Cookie': f"passToken={passToken};userId={userId};deviceId={deviceId};"
}

r = requests.get(f"{base_url}/pass2/profile/home", params={'userId': userId}, headers=headers)

info = parse(r)

phone = info["data"]["phoneModifyTime"]
email = info["data"]["emailModifyTime"]

if phone > email:
    unmasked = info["data"]["unmaskedSafePhone"]
    ctime = phone
    msg = 'phone number'
elif email > phone:
    unmasked = info["data"]["unmaskedSafeEmail"]
    ctime = email
    msg = 'email'
else:
    exit("!")

dt = datetime.fromtimestamp(ctime / 1000)

print(f"\nYour account was created on {dt} (UTC), using a {msg}: {unmasked}.")

print(f"\nNote: If you previously replaced the {msg} with another one, the displayed date is the date of the change, not the original creation date.")

