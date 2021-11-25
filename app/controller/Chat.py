import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')

from model.chatMongo import chatMongo
from model.imoveisMongo import imoveisMongo
from library.myToken import myToken

from flask import request
import datetime

class Chat(object):

    def __init__(self):
        self.chatMongo = chatMongo()
        self.imoveisMongo = imoveisMongo()

    def get(self):
        token = myToken()
        info = token.getInfo()
        filtro = {'usuario_site':info["id"]}
        itens = self.chatMongo.getItens(filtro)
        retorno = []
        for i in itens['itens']:
            e = i
            e['imovel'] = self.imoveisMongo.getItem(i['id_imovel'])
            e['_id'] = str(i['_id'])
            retorno.append(e)
        return retorno

    def set(self):
        token = myToken()
        info = token.getInfo()
        data = json.loads(request.data)
        filtro = {'usuario_site': info["id"], 'id_imovel': data['id_imovel']}
        item = self.chatMongo.getItemFiltro(filtro)
        i = {'autor': 'usuario', 'message': data['message'], 'date': datetime.datetime.now()}
        item['interacao'].append(i)
        salvou = self.chatMongo.update_id(item['_id'], item)
        item['_id'] = str(item['_id'])
        if salvou:
            item["status"] = True
            return item
        item["status"] = False
        return item


    def get_qtde(self):
        token = myToken()
        info = token.getInfo()
        filtro = {'usuario_site': info["id"]}
        itens = self.chatMongo.getItens(filtro)
        return {'qtde':itens['qtde']}
