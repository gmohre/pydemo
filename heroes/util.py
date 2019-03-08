import time
import hashlib

from flask import current_app as app

def marvel_hash():
    ts = str(int(time.time()))
    m = hashlib.md5()
    key = ''.join((
        ts,
        app.config['PRIVATE_API_KEY'],
        app.config['PUBLIC_API_KEY']))
    m.update(key.encode('utf-8'))
    return ts, m.hexdigest(), app.config['PUBLIC_API_KEY']
