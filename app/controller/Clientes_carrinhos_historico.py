#!/usr/bin/python3

import json
import sys


sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.clientesCarrinhosHistoricoModel import clientesCarrinhosHistoricoModel
from model.clientesCarrinhosModel import clientesCarrinhosModel
from flask import request
import time
import datetime

from library.Exception import RequestRetornaZeroItens
from library.Exception import RequestInvalido

class Clientes_carrinhos_historico(object):

    def __init__(self):
        self.clientesCarrinhosHistoricoModel = clientesCarrinhosHistoricoModel()
        self.clientesCarrinhosModel = clientesCarrinhosModel()

    def add(self):
        data = request.get_json()
        if request.content_length > 0:
            if 'clientes_carrinhos' in data:
                update = self.clientesCarrinhosModel.update_id(data['clientes_carrinhos']['data'],data['clientes_carrinhos']['filtro']['id'])
            return self.clientesCarrinhosHistoricoModel.add(data['clientes_carrinhos_historico']['data'])
        return False

    def add_update(self):
        data = request.get_json()
        print(data)
        if request.content_length > 0:
            if 'clientes_carrinhos' in data:
                update = self.clientesCarrinhosModel.update_id(data['clientes_carrinhos']['data'],
                                                               data['clientes_carrinhos']['filtro']['id'])
            return self.clientesCarrinhosHistoricoModel.add(data['clientes_carrinhos_historico']['data'])
        return False



    def requestItems(self):
        data = {}
        for k,v in request.args.items():
            data[k] = v
        return data

    def get(self):
        data = self.requestItems()
        return self.clientesCarrinhosHistoricoModel.getItens(data)


    def getItem(self,id):
        item = self.clientesCarrinhosHistoricoModel.getItem(id, id_empresa)
        if len(item):
            return item
        return False

    def update(self, id):
        item = self.clientesCarrinhosHistoricoModel.getItem(id)
        data = request.get_json()
        if len(item):
            return self.clientesCarrinhosHistoricoModel.update_id(data, id)
        return False

    def delete(self):
        data = request.args
        item = self.clientesCarrinhosHistoricoModel.getItem(data['id'])
        if len(item):
            return self.clientesCarrinhosHistoricoModel.delete_id(data['id'])
        return False


if __name__ == '__main__':
    pass