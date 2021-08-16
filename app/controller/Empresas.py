#!/usr/bin/python3
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from library.myMongo import myMongo

class Empresas(object):

    def __init__(self):
        self.myMongo = myMongo('imoveis')

    def mongoGet(self, data):
        return self.myMongo.get_itens('empresas', {'where': {'cidade_link': data['cidade_link']}, 'sort':{'ordenacao':1}})



if __name__ == '__main__':
    Imoveis.get()
