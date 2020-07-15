#!/usr/bin/python3

import json
import sys

sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.clientesCadastrosModel import clientesCadastrosModel
from flask import request
import time
import datetime

class Clientes_cadastros(object):

    def __init__(self):
        self.clientesCadastrosModel = clientesCadastrosModel()

    def add(self):
        data = request.get_json()
        if request.content_length > 0:
            return self.clientesCadastrosModel.add(data)
        return False

    def get(self):
        data = {}
        for k,v in request.args.items():
            data[k] = v
        return self.clientesCadastrosModel.getItens(data)

    def getItem(self,id, id_empresa):
        item = self.clientesCadastrosModel.getItem(id, id_empresa)
        if len(item):
            return item
        return False

    def update(self, id, id_empresa):
        item = self.clientesCadastrosModel.getItem(id,id_empresa)
        data = request.get_json()
        if 'id_empresa' in data:
            del data['id_empresa']
        if len(item):
            return self.clientesCadastrosModel.update_id(data, id)
        return False

    def delete(self):
        print('del')
        data = request.args
        if 'id_empresa' in data:
            item = self.clientesCadastrosModel.getItem(data['id'], data['id_empresa'])
            if len(item):
                return self.clientesCadastrosModel.delete_id(data['id'])
        return False



if __name__ == '__main__':
    pass