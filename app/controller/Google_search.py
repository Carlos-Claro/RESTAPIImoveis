#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.googlesearchMongo import GooglesearchMongo
from library.myMongo import myMongo
from flask import request
import time
import datetime

class Google_search(object):

    def __init__(self):
        self.googlesearchMongo = GooglesearchMongo()

    def add(self):
        data = json.loads(request.json)
        return {'qtde': self.myMongo.add_one('google_search', data)}

    def get(self):
        data = {}
        for k,v in request.args.items():
            data[k] = v
        return self.googlesearchMongo.getItens(data)

    def getItem(self,id, id_empresa):
        item = self.googlesearchMongo.getItem(id, id_empresa)
        if len(item):
            return item
        return False

    def update(self, id, id_empresa):
        item = self.googlesearchMongo.getItem(id,id_empresa)
        data = request.get_json()
        if 'id_empresa' in data:
            del data['id_empresa']
        if len(item):
            return self.googlesearchMongo.update_id(data, id)
        return False

    def delete(self):
        data = request.args
        if 'id_empresa' in data:
            item = self.googlesearchMongo.getItem(data['id'], data['id_empresa'])
            if len(item):
                return self.googlesearchMongo.delete_id(data['id'])
        return False



if __name__ == '__main__':
    pass
