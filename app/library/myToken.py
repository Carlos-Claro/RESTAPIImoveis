
from flask import request
from .myKeys import myKeys
from jwcrypto import jwt,jwk
import json

class myToken(object):

    def __init__(self):
        keys = myKeys()
        basic = keys.get('basic', False)
        self.KEY_JWK = jwk.JWK(generate='oct', size=256).from_password(basic['user'] + basic['passwd'])



    def set(self, info):
        token = jwt.JWT(header={"alg": "HS256"},
                        claims=info)
        token.make_signed_token(self.KEY_JWK)
        return token.serialize()


    def getInfo(self):
        token = request.headers['authorization'].replace('Bearer ', '').strip()
        ET = jwt.JWT(key=self.KEY_JWK, jwt=token)
        info = json.loads(ET.claims)
        return info

    def refresh(self):
        return 0


