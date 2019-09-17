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
        res_p = self.myMongo.aggregate(pipeline,'log_portal')
        empresas = self.set_soma_dbs_int(res['itens'],res_p['itens'])
        retorno = {}
        for chave,valor in empresas.items():
            retorno[chave] = {}
            retorno[chave]['total_empresa'] = valor
            p2 = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_empresa":chave}},
                {"$group":{"_id":"$tipo","acesso":{"$sum":1}}}
                    ]
            res2 = self.myMongo.aggregate(p2,'log_imoveis')
            res2_p = self.myMongo.aggregate(p2,'log_portal')
            tipos = self.set_soma_dbs_char(res2['itens'],res2_p['itens'])
            for chave_tipo,valor_tipo in tipos.items():
                p3 = [
                    {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_empresa":chave,"tipo":chave_tipo}},
                    {"$group":{"_id":"$id_imovel","acesso":{"$sum":1}}}
                        ]
                res3 = self.myMongo.aggregate(p3,'log_imoveis')
                res3_p = self.myMongo.aggregate(p3,'log_portal')
                imoveis = self.set_soma_dbs_char(res3['itens'],res3_p['itens'])
                lista = []
                for id_imovel,valor_imovel in imoveis.items():
                    lista.append({id_imovel:valor_imovel})
                retorno[chave][chave_tipo] = {'total': valor_tipo,'imoveis':lista}
                del lista
        return retorno
    
    def mongoGetLogImoveisData(self):
        dias = request.args['dias']
        da = datetime.datetime.now() - datetime.timedelta(days=int(dias))
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        pipeline = [
                {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)}}},
                {"$group":{"_id":"$id_imovel","acesso":{"$sum":1}}}
                ]
        res = self.myMongo.aggregate(pipeline,'log_imoveis')
        res_p = self.myMongo.aggregate(pipeline,'log_portal')
        imoveis = self.set_soma_dbs_int(res['itens'],res_p['itens'])
        return imoveis
        
    def mongoGetLogImoveisItem(self):
        dias = request.args['dias']
        da = datetime.datetime.now() - datetime.timedelta(days=int(dias))
        y = int(da.strftime('%Y'))
        m = int(da.strftime('%m'))
        d = int(da.strftime('%d'))
        id_imovel = request.args['id_imovel']
        retorno = {}
        p2 = [
            {"$match":{"data":{"$gte":datetime.datetime(y,m,d,0,0),"$lte":datetime.datetime(y,m,d,23,59)},"id_imovel":int(id_imovel)}},
            {"$group":{"_id":"$tipo","acesso":{"$sum":1}}}
            ]
        res2 = self.myMongo.aggregate(p2,'log_imoveis')
        res2_p = self.myMongo.aggregate(p2,'log_portal')
        tipos = self.set_soma_dbs_char(res2['itens'],res2_p['itens'])
        for chave_tipo,valor_tipo in tipos.items():
            retorno[chave_tipo] = valor_tipo
        return retorno
    
    def set_soma_dbs_int(self,imoveis,portal):
        retorno = {}
        for i in imoveis:
            if i['_id'] is not None and i['_id'] > 0:
                retorno[int(i['_id'])] = i['acesso']
        for p in portal:
            if p['_id'] is not None and p['_id'] > 0:
                c = int(p['_id'])
                if c in retorno:
                    retorno[c] = retorno[c] + p['acesso']
                else:
                    retorno[c] = p['acesso']
        return retorno
    
    def set_soma_dbs_char(self,imoveis,portal):
        retorno = {}
        for i in imoveis:
            if i['_id'] is not None:
                retorno[i['_id']] = i['acesso']
        for p in portal:
            if p['_id'] is not None:
                if p['_id'] in retorno:
                    retorno[p['_id']] = retorno[p['_id']] + p['acesso']
                else:
                    retorno[p['_id']] = p['acesso']
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
    
    def mongoGetLogEmpresaMinData(self):
        pipeline = [
                {"$group":{"_id":{},"data":{"$min":'$data'}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_empresas_dia')
    
    
    def mongoGetLogEmpresaMaxData(self):
        pipeline = [
                {"$group":{"_id":{},"data":{"$max":'$data'}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_empresas_dia')
    
    def mongoGetLogImovelMinData(self):
        pipeline = [
                {"$group":{"_id":{},"data":{"$min":'$data'}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_imoveis_dia')
    
    
    def mongoGetLogImovelMaxData(self):
        pipeline = [
                {"$group":{"_id":{},"data":{"$max":'$data'}}}
                ]
        return self.myMongo.aggregate(pipeline,'log_imoveis_dia')
    
    def add_log_empresa_dia(self):
        args = json.loads(request.get_json())
        data = args['data']
        del args['data']
        args['data'] = datetime.datetime(int(data[0]),int(data[1]),int(data[2]),0,0)
        return {'ok':self.myMongo.add_one('log_empresas_dia',args)}
    
    def add_log_imovel_dia(self):
        args = json.loads(request.get_json())
        data = args['data']
        del args['data']
        args['data'] = datetime.datetime(int(data[0]),int(data[1]),int(data[2]),0,0)
        return {'ok':self.myMongo.add_one('log_imoveis_dia',args)}
    
if __name__ == '__main__':
    Imoveis.get()
    