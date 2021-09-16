#!/usr/bin/python3

import json
import sys

sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.UsuarioPortalMongo import usuarioPortalMongo
from library.myMongo import myMongo


class UsuarioPortal(object):

    def __init__(self):
        self.usuarioPortalMongo = usuarioPortalMongo()
        self.myMongo = myMongo('usuario_portal')

    def add(self, data):
        return self.usuarioPortalMongo.add(data)

    def update(self, id, data):
        return {'qtde': self.usuarioPortalMongo.update_id(data, id)}

    def delete(self, id):
        return {'qtde': self.usuarioPortalMongo.delete_id(id)}

    def get(self):
        return self.usuarioPortalMongo.getItens({'limit': 10})

    def getId(self,id):
        return self.usuarioPortalMongo.getItem(id)



if __name__ == '__main__':
    Usuario_portal.get()

