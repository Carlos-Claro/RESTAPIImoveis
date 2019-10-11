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
    
    def get_in(self,id_empresa):
        get = request.args['id']
        a = json.loads(get);
        ids = []
        for i in a:
            ids.append(i)
        data = {}
        print(ids)
        data['where'] = {'id_' : {'$in':ids}, 'id_empresa':str(id_empresa), 'cidades_id': {'$in': ['9730', '2', '10', '4', '5', '27','1']} }
        value = self.myMongo.get_itens('imoveis',data)
        print(value)
        if len(ids) == value['qtde'] :
            res = {'deleta':False}
        else:
            if value['qtde'] == 0:
                res = {'deleta':True, 'todos':True}
            else:
                res = {'deleta':True, 'ids':[]}
                for item in value['itens']:
                    res['ids'].append(item['id'])
        return res
    
    def get_id_cidade(self,id_):
        data = {}
        data['where'] = {'id' : id_, 'cidades_id': {'$in': ['9730', '2', '10', '4', '5', '27','1']} }
        value = self.myMongo.get_itens('imoveis',data)
        if value['qtde'] == 0 :
            return False
        else:
            return value['itens']
    
    def get_ativos(self):
        data = {}
        data['limit'] = request.args['limit']
        value = self.imoveisModel.getItens_integra(data)
        if value['qtde'] == 0 :
            return False
        else:
            return value['itens']
        
    
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
        return {'qtde':self.myMongo.add_one('imoveis',request.args)}
    
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
        return {'qtde':self.myMongo.delete_one('imoveis',{'_id':int(id)})}
    
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
        if 'id_empresa' in request.args :
            data['where'] = {'tem_foto': False, 'cidades_id': {'$in': ['9730', '2', '10', '4', '5', '27','1']}, 'id_empresa': request.args['id_empresa']}
        else:
            data['where'] = {'tem_foto': False, 'cidades_id': {'$in': ['9730', '2', '10', '4', '5', '27','1']}}
            
        data['sort'] = {'data_update':0, 'cidades_id': 1, 'ordem':0}
        data['limit'] = int(limit)
        return self.myMongo.get_itens('imoveis',data)
    

if __name__ == '__main__':
    Imoveis.get()
    