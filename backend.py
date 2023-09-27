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

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
with open('data.json') as f:
    data = json.load(f)


def check_ticket(ticket, service):
    validate = "https://passport.ustc.edu.cn/serviceValidate?" + urlencode(
        {
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
    service = str(request.base_url) + "?" + urlencode(
        {"hack": ".ustc.edu.cn/"})
    if ticket is None or (uid := check_ticket(ticket, service)) is None:
        return RedirectResponse("https://passport.ustc.edu.cn/login?" +
                                urlencode({"service": service}))

    logging.info(f'{uid} logged in')
    return HTMLResponse(f"""
    <html>
        <head>
            <title>USTC CAS 密信</title>
        </head>
        <body style="margin:30px">
            <h2><a style="text-decoration:none;color:initial;" target="_blank" href="https://github.com/yusanshi/ustc-cas-secret">USTC CAS 密信</a></h2>
            <p>Hi {uid}！{'以下是你的密信：' if uid in data else '找不到你的密信！'}</p>
            <div>{data.get(uid,'')}</div>
        </body>
    </html>
    """)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8088)
