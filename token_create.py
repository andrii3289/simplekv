import hashlib
import time


def token_create():
    obj = hashlib.md5(str(time.time())+"rand")
    token = obj.hexdigest()
    return token
