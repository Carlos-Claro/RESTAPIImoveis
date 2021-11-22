import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')

from model.chatMongo import chatMongo
from library.myToken import myToken

class Chat(object):

    def __init__(self):
        self.chatMongo = chatMongo()

    def get(self):
        token = myToken()
        info = token.getInfo()
        filtro = {'usuario_site':info["id"]}
        itens = self.chatMongo.getItens(filtro)
        retorno = []
        for i in itens['itens']:
            e = i
            e['_id'] = str(i['_id'])
            retorno.append(e)
        return retorno

    def get_qtde(self):
        token = myToken()
        info = token.getInfo()
        filtro = {'usuario_site': info["id"]}
        itens = self.chatMongo.getItens(filtro)
        return {'qtde':itens['qtde']}
