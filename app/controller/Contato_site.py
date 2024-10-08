#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.contatoSiteModel import contatoSiteModel
from model.logPortalMongo import logPortalMongo
from model.chatMongo import chatMongo
from model.UsuarioPortalMongo import usuarioPortalMongo
from library.myToken import myToken
from library.mySMTP import mySMTP
from flask import request
import time
import datetime



class Contato_site(object):

    def __init__(self):
        self.contatoSiteModel = contatoSiteModel()
        self.logPortalMongo = logPortalMongo()
        self.chatMongo = chatMongo()
        self.usuarioPortalMongo = usuarioPortalMongo()

    def set(self):
        retorno = {"status":False, "message": "Não foi possivel processar a requisição"}
        token = myToken()
        info = token.getInfo()
        usuario = self.usuarioPortalMongo.getItem(info['id'])
        data_add = {'usuario_portal': info['id'],
                    'ip': request.remote_addr,
                    'host': request.headers['origin'],
                    'data': datetime.datetime.now()
                    }
        data = json.loads(request.data)
        data_add['tipo'] = 'contato_site'
        data_add['id_empresa'] = data['id_empresa']
        data_add['id_imovel'] = int(data['id_imovel'])
        id = self.logPortalMongo.add(data_add)
        contato_site = data.copy()
        contato_site['portal'] = data_add['host']
        contato_site['mensagem'] = contato_site['message']
        contato_site['email'] = usuario['email']
        contato_site['nome'] = usuario['nome']
        del contato_site['message']
        del contato_site['id_imovel']
        del contato_site['referencia']
        link = contato_site['link']
        del contato_site['link']
        contato_site['data'] = int(time.time())
        id_contato = self.contatoSiteModel.add(contato_site)
        if id_contato:
            # todo: disparo de email
            contato_site['link'] = link
            smtp = mySMTP(contato_site)
            smtp.envioEmpresa()
            smtp.envioUsuario()
            retorno = {"status": True, "message": "Mensagem salva, a imobiliaria foi avisada da sua dúvida"}
            verificaChatAtivo = self.chatMongo.getItemFiltro({'usuario_site':info['id'], 'id_imovel': int(data['id_imovel'])})
            if verificaChatAtivo:
                # todo: adiciona interacao
                print(verificaChatAtivo)
                pass
            else:
                data_add_chat = {
                    'id_contato_site': id_contato,
                    'usuario_site': info['id'],
                    'id_empresa': int(data['id_empresa']),
                    'id_imovel': int(data['id_imovel']),
                    'status': True,
                    'status_interacao':0,
                    'link':link,
                    'date':datetime.datetime.now(),
                    'interacao': [{'autor':'usuario', 'message': data['message'], 'date':datetime.datetime.now()}]
                }
                id_chat = self.chatMongo.add(data_add_chat)
                if id_chat:
                    retorno = {"status": True, "message": "Mensagem salva, e enviada para a imobiliaria, consulte a conversa no chat"}
                else:
                    pass
        return retorno

    def setEmailEmpresa(self, data):
        return 0

    def setEmailUsuario(self, data):
        return 0

    def getContatos(self):
        return self.contatoSiteModel.getItensDisparo(request.args)

    def update_sincronizado(self):
        ids = request.args['ids']
        print(ids)
        return self.contatoSiteModel.update_id_in({'sincronizado': 1}, ids)

    def update_desincronizado(self):
        ids = request.args['ids']
        return self.contatoSiteModel.update_id_in({'sincronizado': 0}, ids)


if __name__ == '__main__':
    Imoveis.get()
