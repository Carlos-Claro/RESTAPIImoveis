#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from imoveisModel import imoveisModel
from imoveisMongo import imoveisMongo
from flask import request
import time

class Imoveis(object):
    
    def __init__(self):
        self.imoveisModel = imoveisModel()
        self.imoveisMongo = imoveisMongo()

    def add(self):
        return {'id': self.imoveisModel.add(request.args)}
        
    def add_test(self,data):
        return {'id': self.imoveisModel.add(data)}
        
    
    def update(self,id):
        return {'qtde': self.imoveisModel.update_id(request.args,id)}
    
    def update_test(self,id,data):
        return {'qtde': self.imoveisModel.update_id(data,id)}
    
    def delete(self,id):
        return {'qtde':self.imoveisModel.delete_id(id)}
    
    def get(self):
        return self.imoveisModel.getItens()
    
    def get_id(self,id):
        return self.imoveisModel.getItem(id)
    
    def get_images_id_empresa(self,id):
        return self.imoveisModel.getImagesIDempresa(id)
    
    def add_images_imovel(self):
        return {'id':self.imoveisModel.getImagesIDimovel(request.args)}
    
    def add_images_imovel_test(self,data):
        return {'id':self.imoveisModel.add_images(data)}
    
    def update_images_id(self,id):
        return {'qtde':self.imoveisModel.update_images_id(request.args,id)}
    
    def update_images_id_test(self,id,data):
        return {'qtde':self.imoveisModel.update_images_id(data,id)}
    
    def delete_images_id(self,id):
        return {'qtde':self.imoveisModel.delete_images_id(id)}
    
    def delete_images_id_imovel(self,id):
        return {'qtde':self.imoveisModel.delete_images_id_imovel(id)}
    
    
    
    
    def mongoAdd(self):
        return request.args
    
    def mongoUpdate(self,id,data):
        #imoveismodel = imoveisModel()
        #return imoveis
        return {'teste':'rrr'}
    
    def mongoDelete(self,id):
        #imoveismodel = imoveisModel()
        #return imoveis
        return {'teste':'rrr'}
    
    def mongoGet(self):
        imoveis = self.imoveisModel.getItens()
        return imoveis
        
    def imagesIDEmpresa(self,idEmpresa):
        return self.imoveisModel.getImagesIDempresaHTTP(idEmpresa)
    
    def imagesGerar(self,limit):
        return self.imoveisModel.getImagesGerar(limit)
    
    
if __name__ == '__main__':
    Imoveis.get()
    