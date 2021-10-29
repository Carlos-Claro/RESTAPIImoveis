#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.logPortalMongo import logPortalMongo
from model.imoveisMongo import imoveisMongo
from flask import request
import time
import datetime
from jwcrypto import jwt,jwk

class Log_portal(object):

    def __init__(self):
        self.logPortalMongo = logPortalMongo()

    def set(self, key):
        token = request.headers['authorization'].replace('Bearer ', '').strip()
        ET = jwt.JWT(key=key, jwt=token)
        info = json.loads(ET.claims)
        data_add = {'usuario_portal': info['id'],
                  'ip': request.remote_addr,
                  'host': request.headers['origin'],
                  'data': datetime.datetime.now()
                  }
        data = json.loads(request.data)
        data_add['tipo'] = data['tipo']
        imoveis = imoveisMongo()
        imovel = imoveis.getItemFiltro({"_id":int(data['id'])})
        data_add['id_empresa'] = imovel['id_empresa']
        data_add['id_imovel'] = imovel['_id']
        data_add['imoveis_tipos_link'] = imovel['imoveis_tipos_link']
        data_add['tipo_negocio'] = imovel['tipo']
        data_add['preco'] = imovel['preco_locacao']
        if 'venda' in  imovel['tipo']:
            data_add['preco'] = imovel['preco_venda']
        data_add['bairros_link'] = imovel['bairros_link']
        data_add['cidades_link'] = imovel['cidades_link']
        data_add['ordem'] = imovel['ordem']
        id = self.logPortalMongo.add(data_add)
        print(id)
        if id:
            return True
        return False



    def add(self, data):
        print('log_pesquisa add')
        print(pesquisa)
        data.update(pesquisa)
        print(data)
        return {'id': self.logPortalMongo.add(data)}


    def get(self):
        data = {}
        for k,v in request.args.items():
            data[k] = v
        return self.logPortalMongo.getItens(data)

    def getItem(self,id):
        item = self.logPortalMongo.getItem(id)
        if len(item):
            return item
        return False

    def update(self, id, data):
        item = self.logPortalMongo.getItem(id)
        if len(item):
            return self.logPortalMongo.update_id(data, id)
        return False

    def update_filtro(self, filtro, data):
        return self.logPortalMongo.update_filtro(filtro, data)


    def delete(self, data):
        data = request.args
        item = self.logPortalMongo.getItem(data['id'])
        if item:
            return self.logPortalMongo.delete_id(data['id'])
        return False



if __name__ == '__main__':
    pass
