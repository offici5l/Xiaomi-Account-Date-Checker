#!/usr/bin/python

from datetime import datetime

import migate
from migate.config import PROFILE_HOME_URL, SECURITY_HOME_URL
from migate.requester import get, parse_res

cookies = migate.get_passtoken()

r = get(PROFILE_HOME_URL, cookies=cookies)
r_text = parse_res(r)
phone = r_text["data"]["phoneModifyTime"]
email = r_text["data"]["emailModifyTime"]
pwd = r_text["data"]["pwdUpdateTime"]

r = get(SECURITY_HOME_URL, cookies=cookies)
r_text = parse_res(r)
phone_1 = r_text["data"]["phoneModifyTime"]
email_1 = r_text["data"]["emailModifyTime"]
pwd_1 = r_text["data"]["pwdUpdateTime"]

if pwd == 0 and pwd_1 > 0:
    dt = datetime.fromtimestamp(pwd_1 / 1000)
    if pwd_1 == email:
        e = r_text["data"]["unmaskedSafeEmail"]
        print(f"\nYour account was created on {dt} (UTC), using a email: {e}\n")
    elif pwd_1 == phone:
        p = r_text["data"]["unmaskedSafePhone"]
        print(f"\nYour account was created on {dt} (UTC), using a phone: {p}\n")
    else:
        print(f"\nYour account was created on {dt} (UTC)\n")


