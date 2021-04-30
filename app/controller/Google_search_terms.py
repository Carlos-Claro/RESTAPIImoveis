#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.googlesearchtermsMongo import GooglesearchtermsMongo
from library.myMongo import myMongo
from flask import request
import time
import datetime

class Google_search_terms(object):

    def __init__(self):
        self.googlesearchtermsMongo = GooglesearchtermsMongo()

    def add(self):
        data = json.loads(request.data)
        if request.content_length > 0:
            return self.googlesearchtermsMongo.add(data)
        return False

    def get(self):
        retorno = self.googlesearchtermsMongo.getItens({})
        print(retorno)
        return retorno

    def getItem(self,id, id_empresa):
        item = self.googlesearchtermsMongo.getItem(id, id_empresa)
        if len(item):
            return item
        return False

    def update(self, id, id_empresa):
        item = self.googlesearchtermsMongo.getItem(id,id_empresa)
        data = request.get_json()
        if 'id_empresa' in data:
            del data['id_empresa']
        if len(item):
            return self.googlesearchtermsMongo.update_id(data, id)
        return False

    def delete(self):
        data = request.args
        if 'id_empresa' in data:
            item = self.googlesearchtermsMongo.getItem(data['id'], data['id_empresa'])
            if len(item):
                return self.googlesearchtermsModngo.delete_id(data['id'])
        return False



if __name__ == '__main__':
    pass
