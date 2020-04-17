#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.contatoSiteModel import contatoSiteModel
from flask import request
import time
import datetime

class Contato_site(object):

    def __init__(self):
        self.contatoSiteModel = contatoSiteModel()

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
