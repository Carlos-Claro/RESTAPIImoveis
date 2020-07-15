#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.produtosModel import ProdutosModel
from flask import request
import time
import datetime

class Produtos(object):

    def __init__(self):
        self.produtosModel = ProdutosModel()

    def add(self):
        data = request.get_json()
        if request.content_length > 0:
            return self.produtosModel.add(data)
        return False

    def get(self):
        data = {}
        for k,v in request.args.items():
            data[k] = v
        return self.produtosModel.getItens(data)

    def getItem(self,id, id_empresa):
        item = self.produtosModel.getItem(id, id_empresa)
        if len(item):
            return item
        return False

    def update(self, id, id_empresa):
        item = self.produtosModel.getItem(id,id_empresa)
        data = request.get_json()
        if 'id_empresa' in data:
            del data['id_empresa']
        if len(item):
            return self.produtosModel.update_id(data, id)
        return False

    def delete(self):
        data = request.args
        if 'id_empresa' in data:
            item = self.produtosModel.getItem(data['id'], data['id_empresa'])
            if len(item):
                return self.produtosModel.delete_id(data['id'])
        return False



if __name__ == '__main__':
    pass
