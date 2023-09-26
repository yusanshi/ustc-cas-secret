"""based on https://github.com/zzh1996/ustccas-revproxy/blob/master/auth/auth_server.py"""

import json
import uvicorn
import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from xml.etree import ElementTree
from urllib.request import urlopen

PORT = 8088
VALIDATE_URL = "https://passport.ustc.edu.cn/serviceValidate"
CAS_URL = "https://passport.ustc.edu.cn/login"
REDIRECT_URL = "http://home.ustc.edu.cn/~liulangcao/cas-redirect.html"

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
with open('data.json') as f:
    data = json.load(f)


def check_ticket(ticket, service):
    validate = VALIDATE_URL + "?" + urlencode({
        "service": service,
        "ticket": ticket
    })
    with urlopen(validate) as req:
        tree = ElementTree.fromstring(req.read())[0]
    cas = "{http://www.yale.edu/tp/cas}"
    if tree.tag != cas + "authenticationSuccess":
        return None
    uid = tree.find(cas + "user").text.strip().upper()
    return uid


@app.get('/')
def main(request: Request, ticket=None):
    service = REDIRECT_URL + "?" + urlencode({"target": request.base_url})
    if ticket is None or (uid := check_ticket(ticket, service)) is None:
        return RedirectResponse(CAS_URL + "?" +
                                urlencode({"service": service}))

    logging.info(f'{uid} logged in')
    return HTMLResponse(f"""
    <html>
        <head>
            <title>USTC CAS 密信</title>
        </head>
        <body style="margin:30px">
            <h3><a style="text-decoration:none;color:initial;" target="_blank" href="https://github.com/yusanshi/ustc-cas-secret">USTC CAS 密信</a></h3>
            <p>Hi {uid}！{'以下是你的密信：' if uid in data else '找不到你的密信！'}</p>
            <div>{data.get(uid,'')}<div>
        </body>
    </html>
    """)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=PORT)
