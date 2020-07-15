#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.clientesCarrinhosProdutosModel import clientesCarrinhosProdutosModel
from flask import request
import time
import datetime

class Clientes_carrinhos_produtos(object):

    def __init__(self):
        self.clientesCarrinhosProdutosModel = clientesCarrinhosProdutosModel()

    def add(self):
        data = request.get_json()
        if request.content_length > 0:
            return self.clientesCarrinhosProdutosModel.add(data)
        return False

    def get(self):
        data = {}
        for k,v in request.args.items():
            data[k] = v
        return self.clientesCarrinhosProdutosModel.getItens(data)

    def getItem(self,id, id_empresa):
        item = self.clientesCarrinhosProdutosModel.getItem(id, id_empresa)
        if len(item):
            return item
        return False

    def update(self, id, id_empresa):
        item = self.clientesCarrinhosProdutosModel.getItem(id,id_empresa)
        data = request.get_json()
        if 'id_empresa' in data:
            del data['id_empresa']
        if len(item):
            return self.clientesCarrinhosProdutosModel.update_id(data, id)
        return False

    def delete(self):
        data = request.args
        if 'id_empresa' in data:
            item = self.clientesCarrinhosProdutosModel.getItem(data['id'], data['id_empresa'])
            if len(item):
                return self.clientesCarrinhosProdutosModel.delete_id(data['id'])
        return False



if __name__ == '__main__':
    Imoveis.get()
