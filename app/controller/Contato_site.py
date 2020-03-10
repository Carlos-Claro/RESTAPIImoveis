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
        return {'contatos': self.contatoSiteModel.getItensDisparo(request.args)}




if __name__ == '__main__':
    Imoveis.get()
