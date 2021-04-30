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
        return self.imoveisModel.getItens_integra({'limit':10})
    
    def get_in(self,id_empresa):
        get = request.args['id']
        a = json.loads(get);
        ids = []
        for i in a:
            ids.append(i)
        data = {}
        # print(ids)
        data['where'] = {'id_' : {'$in':ids}, 'id_empresa':str(id_empresa), 'cidades_id': {'$in': ['9730', '2', '10', '4', '5', '27','1']} }
        value = self.myMongo.get_itens('imoveis',data)
        # print(value)
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
    
    def set_args(self,array):
        retorno = {}
        for k,v in array.items():
            retorno[k] = v
        return retorno
    
    def alteraDatas(self,item):
        retorno = self.set_args(item)
        retorno['data_update'] = datetime.datetime.now()
        return retorno
    
    def mongoAdd(self):
        data = self.alteraDatas(json.loads(request.json))
        item = self.mongoGetId(data['_id'])
        if item:
            return {'qtde':self.myMongo.update_one('imoveis',{'_id': data['_id']}, data)}
        return {'qtde':self.myMongo.add_one('imoveis',data)}
    
    def mongoUpdate(self,id,data):
        alt = {}
        for k,v in data.items():
            if 'tem_foto' in k:
                # print('tem_ft')
                alt[k] = bool(v)
            else:
                alt[k] = v
        return {'qtde':self.myMongo.update_one('imoveis',{'_id':int(id)},alt)}
    
    def mongoDelete(self,id):
        return {'qtde':self.myMongo.delete_one('imoveis',{'_id':int(id)})}
    
    
    # array com ['limit', ''skip', coluna, ordem]
    #
    #
    def mongoGet(self, data):
        retorno = {}
        retorno['itens'] = self.myMongo.get_itens('imoveis',self.setDataPesquisa(data))
        retorno['qtde_total'] = self.myMongo.get_total_itens('imoveis',self.setDataPesquisa(data))
        return retorno
        
    def setDataPesquisa(self,data):
        args = {}
        for k,v in data.items():
            args[k] = v
        retorno = {}
        retorno['limit'] = 10
        if 'limit' in args:
            retorno['limit'] = int(args['limit'])
            del args['limit']
        if 'skip' in args:
            retorno['skip'] = int(args['skip'])
            del args['skip']
        retorno['sort'] = {'ordem':-1}
        if 'coluna' in args or 'ordem' in args:
            ordem = self.getOrdenacao(args);
            retorno['sort'] = {ordem[0]:ordem[1]}
            # print(retorno['sort'])
            if 'coluna' in args:
                del args['coluna']
            if 'ordem' in args:
                del args['ordem']
        # print(args)
        if len(args) > 0:
            retorno['where'] = self.getWhere(args)
        return retorno
    isfloat = []
    isint = ['quartos','garagens','id_tipo','cidades_id']
    
    def getOrdenacao(self,data):
        coluna = 'ordem'
        if data['coluna'] in ['min','max']:
            a = data['coluna'].split('-')
            coluna = a[0]
            if a[1] == 'min':
                ordem = 1
            else: 
                ordem = -1
        else:
            coluna = data['coluna']
            ordem = -1
        return [coluna,ordem];
    
    def getItemVirgula(self,valor,tipo):
        isin = False
        if ',' in valor:
            isin = True
            array = valor.split(',')
            v = []
            for a in array:
                v.append(self.getValorTipo(a,tipo))
        else:
            v = self.getValorTipo(valor,tipo)
        return v,isin
    
    def getValorTipo(self,valor,tipo):
        if tipo:
            if 'int' in tipo:
                return int(valor)
            return valor
        return valor
        
    
    def getWhere(self,itens):
        retorno = {}
        for chave,valor in itens.items():
            # print(chave)
            if chave in self.isint:
                v,isin = self.getItemVirgula(valor,'int')
            else :
                v,isin = self.getItemVirgula(valor,False)
            retorno[chave] = v
            if isin:
                retorno[chave] = {'$in':v}
        return retorno
    
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
            data['where'] = {'tem_foto': False, 'cidades_id': {'$in': [9730, 2, 10, 4, 5, 27,1]}, 'id_empresa': request.args['id_empresa']}
        else:
            data['where'] = {'tem_foto': False, 'cidades_id': {'$in': [9730, 2, 10, 4, 5, 27,1]}}
            
        data['sort'] = {'data_update':0, 'cidades_id': 1, 'ordem':0}
        data['limit'] = int(limit)
        return self.myMongo.get_itens('imoveis',data)
    

if __name__ == '__main__':
    Imoveis.get()
    
