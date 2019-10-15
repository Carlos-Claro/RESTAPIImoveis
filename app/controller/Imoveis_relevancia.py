#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from model.imoveisModel import imoveisModel
from model.imoveisMongo import imoveisMongo
from library.myMongo import myMongo
from flask import request
import time
import datetime

class Imoveis_relevancia(object):
    
    def __init__(self):
        self.imoveisRelevanciaModel = imoveisRelevanciaModel()

    def add(self):
        return {'id': self.imoveisRelevanciaModel.add(request.args)}
        
    def add_test(self,data):
        return {'id': self.imoveisRelevanciaModel.add(data)}
        
    
    def update(self,id):
        return {'qtde': self.imoveisRelevanciaModel.update_id(request.args,id)}
    
    def update_test(self,id,data):
        return {'qtde': self.imoveisRelevanciaModel.update_id(data,id)}
    
    def delete(self,id):
        return {'qtde':self.imoveisRelevanciaModel.delete_id(id)}
    
    def get(self):
        return self.imoveisRelevanciaModel.getItens(request.args)
    
    def get_total(self):
        return self.imoveisRelevanciaModel.getTotalItens(request.args)
    
    def add_log(self):
        return {'id': self.imoveisRelevanciaModel.add_log(request.args)}
        
    def update_log(self,id):
        return {'qtde': self.imoveisRelevanciaModel.update_id_log(request.args,id)}
    
    def delete_log(self,id):
        return {'qtde':self.imoveisRelevanciaModel.delete_id_log(id)}
    
    def get_log(self):
        return self.imoveisRelevanciaModel.getItens_log(request.args)
    
    def get_total_log(self):
        return self.imoveisRelevanciaModel.getTotalItens_log(request.args)
    
if __name__ == '__main__':
    print('')
    
