#!/usr/bin/python3

import json
import sys


sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.clientesCarrinhosModel import clientesCarrinhosModel
from model.clientesCarrinhosProdutosModel import clientesCarrinhosProdutosModel
from flask import request
import time
import datetime

from library.Exception import RequestRetornaZeroItens

class Clientes_carrinhos(object):

    def __init__(self):
        self.clientesCarrinhosModel = clientesCarrinhosModel()

    def add(self):
        data = request.get_json()
        if request.content_length > 0:
            return self.clientesCarrinhosModel.add(data)
        return False

    def requestItems(self):
        data = {}
        for k,v in request.args.items():
            data[k] = v
        return data

    def get(self):
        data = self.requestItems()
        return self.clientesCarrinhosModel.getItens(data)

    def getCompleto(self):
        data = self.requestItems()
        carrinhos = self.clientesCarrinhosModel.getItens(data)
        print(carrinhos)
        retorno = []
        if carrinhos['total']:
            carrinhosProdutosModel = clientesCarrinhosProdutosModel()
            for i in carrinhos['itens']:
                filtro = {}
                filtro["id_empresa"] = data['id_empresa']
                filtro["id_clientes_carrinhos"] = str(i['id'])
                filtro["limit"] = 1000
                i['produtos'] = carrinhosProdutosModel.getItensCompleto(filtro)
                retorno.append(i)
        else:
            raise RequestRetornaZeroItens('Nenhum item retornado para carrinho completo')
        return retorno

    def getItem(self,id, id_empresa):
        item = self.clientesCarrinhosModel.getItem(id, id_empresa)
        if len(item):
            return item
        return False

    def update(self, id, id_empresa):
        item = self.clientesCarrinhosModel.getItem(id,id_empresa)
        data = request.get_json()
        if 'id_empresa' in data:
            del data['id_empresa']
        if len(item):
            return self.clientesCarrinhosModel.update_id(data, id)
        return False

    def delete(self):
        data = request.args
        if 'id_empresa' in data:
            item = self.clientesCarrinhosModel.getItem(data['id'], data['id_empresa'])
            if len(item):
                return self.clientesCarrinhosModel.delete_id(data['id'])
        return False



if __name__ == '__main__':
    Imoveis.get()
