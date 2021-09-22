#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.logPesquisasMongo import logPesquisasMongo
from flask import request
import time
import datetime

class Log_pesquisas(object):

    def __init__(self):
        self.logPesquisasMongo = logPesquisasMongo()

    def add(self, data, pesquisa):
        print('log_pesquisa add')
        print(pesquisa)
        data.update(pesquisa)
        print(data)
        return {'id': self.logPesquisasMongo.add(data)}

    log_campos = {

    }

    def processa_pesquisa(self,data):
        return {}

    def get(self):
        data = {}
        for k,v in request.args.items():
            data[k] = v
        return self.logPesquisasMongo.getItens(data)

    def getItem(self,id):
        item = self.logPesquisasMongo.getItem(id)
        if len(item):
            return item
        return False

    def update(self, id, data):
        item = self.logPesquisasMongo.getItem(id)
        if len(item):
            return self.logPesquisasMongo.update_id(data, id)
        return False

    def delete(self, data):
        data = request.args
        item = self.logPesquisasMongo.getItem(data['id'])
        if item:
            return self.logPesquisasMongo.delete_id(data['id'])
        return False



if __name__ == '__main__':
    pass
