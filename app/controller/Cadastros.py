#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.cadastrosModel import cadastrosModel
from flask import request
import time
import datetime

class Cadastros(object):

    def __init__(self):
        self.cadastrosModel = cadastrosModel()

    def update_sincronizado(self,id):
        return self.cadastrosModel.update_id({'sincronizado':1},id)

    def update_desincronizado(self,id):
        return self.cadastrosModel.update_id({'sincronizado':0},id)




if __name__ == '__main__':
    pass
