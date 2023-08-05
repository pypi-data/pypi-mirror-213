import time

import requests
import datetime
import random

# from

if __name__ == '__main__':
    login = "http://10.112.7.131/gateway/omsp-base-service/sys/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    resp_login = requests.post(login, headers=headers, data={"username": "pei.xiaodong", "password": "Qq.2921481"})
    token = resp_login.json()['data']['token']
    print(token)
    dt = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 8,
                           52, random.randint(0, 59))
    time.sleep(1)
    print(dt)
    timestamp = int(time.mktime(dt.timetuple()))
    print(timestamp)
    dk = f"http://10.112.7.131/gateway/omsp-base-service/attend/signIn?_t={timestamp}"
    resp = requests.get(dk, headers={"cookie": "JSESSIONID=73ec7f0d-d6b0-42fd-8390-4f8ac82dbf00", "token": token, 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"})
    print(resp.content.decode())
    debug = True
    print("---------------------------")
    print(datetime.datetime.now())
    print("---------------------------")
    # dk2 = "http://10.112.7.131/gateway/omsp-base-service/attend/signOut?_t=167636888"
    # resp = requests.get(dk2, headers={"cookie": "JSESSIONID=73ec7f0d-d6b0-42fd-8390-4f8ac82dbf00", "token": token})
    # print(resp.content.decode())
