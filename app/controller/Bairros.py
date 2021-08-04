#!/usr/bin/python3

import json
import sys

sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from library.myMongo import myMongo



class Bairros(object):

    def __init__(self):
        self.myMongo = myMongo('imoveis')

    def mongoGet(self, data):
        bairros = self.myMongo.get_itens('bairros', {'where': {'cidade_link': data}})
        return bairros

    def setDataPesquisa(self, data):
        retorno = {}
        print(data)
        retorno = {'dominio': {'$regex': data}}
        return retorno

    def mongoGetinID(self, data):
        bairros = self.myMongo.get_itens('bairros', {'where': {'id': {'$in': data}}})
        return bairros


if __name__ == '__main__':
    pass
