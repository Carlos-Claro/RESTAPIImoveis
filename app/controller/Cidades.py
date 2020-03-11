#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from library.myMongo import myMongo
from flask import request
import time
import datetime

class Cidades(object):
    
    def __init__(self):
        self.myMongo = myMongo('imoveis')

    def mongoGet(self, data):
        cidade = self.myMongo.get_item_filtro('cidades',self.setDataPesquisa(data))
        cidade['bairros'] = self.myMongo.get_itens('bairros',{'where':{'cidade_link':cidade['link']}})
        return cidade

    def setDataPesquisa(self,data):
        retorno = {}
        print(data)
        retorno = {'dominio':{'$regex':data}}
        return retorno

    def mongoGetinID(self, data):
        cidades = self.myMongo.get_itens('cidades',{'where':{'id':{'$in':data}}})
        return cidades
    
if __name__ == '__main__':
    Imoveis.get()
    