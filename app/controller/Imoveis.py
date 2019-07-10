#!/usr/bin/python3

import json
import sys
sys.path.append('../library')
sys.path.append('../controller')
sys.path.append('../model')
from imoveisModel import imoveisModel
from imoveisMongo import imoveisMongo
from myMongo import myMongo
from flask import request
import time

class Imoveis(object):
    
    def __init__(self):
        self.imoveisModel = imoveisModel()
        self.imoveisMongo = imoveisMongo()
        self.myMongo = myMongo('imoveis')

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
    
    def update_images_id_imovel(self,id):
        return {'qtde':self.imoveisModel.update_images_id_imovel(request.args,id)}
    
    def update_images(self):
        retorno = 0
        data = request.args
        id = data['id']
        i = self.imoveisModel.update_images_id(data,id)
        return {'qtde':i}
    
    def update_images_id_test(self,id,data):
        return {'qtde':self.imoveisModel.update_images_id(data,id)}
    
    def delete_images_id(self,id):
        return {'qtde':self.imoveisModel.delete_images_id(id)}
    
    def delete_images_id_imovel(self,id):
        return {'qtde':self.imoveisModel.delete_images_id_imovel(id)}
    
    
    
    
    def mongoAdd(self):
        return request.args
    
    def mongoUpdate(self,id,data):
        alt = {}
        for k,v in data.items():
            if 'tem_foto' in k:
                print('tem_ft')
                alt[k] = bool(v)
            else:
                alt[k] = v
        return {'qtde':self.myMongo.update_one('imoveis',{'_id':int(id)},alt)}
    
    def mongoDelete(self,id):
        #imoveismodel = imoveisModel()
        #return imoveis
        return {'teste':'rrr'}
    
    def mongoGet(self):
        imoveis = self.imoveisModel.getItens()
        return imoveis
        
    def mongoGetId(self,id):
        imoveis = self.myMongo.get_item('imoveis',id)
        return imoveis
        
    def imagesIDEmpresa(self,idEmpresa):
        return self.imoveisModel.getImagesIDempresaHTTP(idEmpresa)
    
    def imagesGerar(self,limit):
        return self.imoveisModel.getImagesGerar(limit)
    
    def imagesGerarMongo(self,limit):
        data = {}
        data['where'] = {'tem_foto': False, 'cidades_id': {'$gt': '0'}}
        data['sort'] = {'data_update':0, 'cidades_id': 1, 'ordem':0}
        data['limit'] = int(limit)
        return self.myMongo.get_itens('imoveis',data)
    
    
if __name__ == '__main__':
    Imoveis.get()
    