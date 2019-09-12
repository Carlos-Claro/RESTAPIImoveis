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
        data['where'] = {'tem_foto': False, 'cidades_id': {'$in': ['9730', '2', '10', '4', '5', '27','1']}}
        data['sort'] = {'data_update':0, 'cidades_id': 1, 'ordem':0}
        data['limit'] = int(limit)
        return self.myMongo.get_itens('imoveis',data)
    
###########################
        #   Estatisticas
        #
        #
###########################
    def mongoGetLogEmpresaData(self):
        dias = request.args['dias']
        da = datetime.datetime.now() - datetime.timedelta(days=int(dias))
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        pipeline = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)}}},
                {"$group":{"_id":"$id_empresa","acesso":{"$sum":1}}}
                ]
        res = self.myMongo.aggregate(pipeline,'log_imoveis')
        retorno = {}
        for item in res['itens']:
            if item['_id'] is not None and item['_id'] > 0:
                retorno[item['_id']] = {}
                retorno[item['_id']]['total_empresa'] = item['acesso']
                p2 = [
                    {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_empresa":item['_id']}},
                    {"$group":{"_id":"$tipo","acesso":{"$sum":1}}}
                        ]
                res2 = self.myMongo.aggregate(p2,'log_imoveis')
                for tipo in res2['itens']:
                    p3 = [
                        {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_empresa":item['_id'],"tipo":tipo['_id']}},
                        {"$group":{"_id":"$id_imovel","acesso":{"$sum":1}}}
                            ]
                    res3 = self.myMongo.aggregate(p3,'log_imoveis')
                    lista = []
                    for id_imovel in res3['itens']:
                        lista.append({id_imovel['_id']:id_imovel['acesso']})
                    if tipo['_id'] is not None:
                        retorno[item['_id']][tipo['_id']] = {'total': tipo['acesso'],'imoveis':lista}
                    del lista
        return retorno
    
    def mongoGetLogImoveisTipo(self):
        dias = request.args['dias']
        imovel = request.args['imovel']
        da = datetime.datetime.now() - datetime.timedelta(days=int(dias))
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        pipeline = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_imovel":imovel}},
                {"$group":{"_id":"$tipo","acesso":{"$sum":1}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_imoveis')
    
    def mongoGetLogPortalData(self):
        data = request.args['data']
        pipeline = [
                {"$match":{"data":{"$gte":data}}},
                {"$group":{"_id":"$id_imovel","acesso":{"$sum":1}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_portal')
    
    def add_log_empresa_dia(self):
        args = json.loads(request.get_json())
        print(args)
        return {'_id':self.myMongo.add_one('log_empresa_dia',args)}
    
if __name__ == '__main__':
    Imoveis.get()
    